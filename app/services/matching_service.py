from sklearn.metrics.pairwise import cosine_similarity
from app.models.post import Post
from app.models.notification import Notification
from app import db
import logging
import os
import shelve
import hashlib
import google.genai as genai
from dotenv import load_dotenv

load_dotenv()

CACHE_PATH = "./embedding_cache"

class MatchingService:
    def __init__(self):
        try:
            self.embedding_model = "gemini-embedding-001"
            # Test the setup
            test_embedding = self._get_embedding("Test")
            if test_embedding is not None:
                logging.info("Matching service initialized successfully")
            else:
                logging.error("Failed to generate test embedding")
                self.embedding_model = None
        except Exception as e:
            logging.error(f"Error initializing matching service: {e}")
            self.embedding_model = None

    def _get_text_hash(self, text):
        return hashlib.md5(text.encode()).hexdigest()

    def _get_embedding(self, text):
        """Helper method to get embeddings with shelve disk caching"""
        try:
            text_hash = self._get_text_hash(text)

            with shelve.open(CACHE_PATH) as cache:
                if text_hash in cache:
                    logging.info(f"Cache hit for text hash: {text_hash}")
                    return cache[text_hash]

            client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
            result = client.models.embed_content(
                model=self.embedding_model,
                contents=text
            )
            embedding = result.embeddings[0].values

            with shelve.open(CACHE_PATH) as cache:
                cache[text_hash] = embedding

            return embedding
        except Exception as e:
            logging.error(f"Error in embedding generation/caching: {e}")
            return None

    def compute_text_similarity(self, text1, text2):
        if not text1 or not text2 or not self.embedding_model:
            return 0

        try:
            # Generate embeddings using Google's Generative AI
            embedding1 = self._get_embedding(text1)
            embedding2 = self._get_embedding(text2)

            # print("Embedding1:", embedding1)  # Debug log
            # print("Embedding2:", embedding2)  # Debug log

            if embedding1 is None or embedding2 is None:
                return 0

            # Calculate cosine similarity
            similarity = float(cosine_similarity([embedding1], [embedding2])[0][0])
            logging.debug(f"Similarity score: {similarity}")
            return similarity
        except Exception as e:
            logging.error(f"Error computing similarity: {e}")
            return 0

    def find_matches(self, post, threshold=0.5):  # Lower threshold for better matches
        try:
            matches = []
            opposite_type = "found" if post.type == "lost" else "lost"
            potential_matches = Post.query.filter_by(type=opposite_type).all()

            for candidate in potential_matches:
                if candidate.id == post.id:
                    continue

                post_text = (f"{post.item_name} {post.description} "
                           f"{post.category_name} {post.location}")
                candidate_text = (f"{candidate.item_name} {candidate.description} "
                                f"{candidate.category_name} {candidate.location}")

                # Calculate similarity score
                print("Calling compute_text_similarity")  # Debug log
                score = self.compute_text_similarity(post_text, candidate_text)
                print("Score:", score)  # Debug log

                # Add category bonus
                if post.category_name == candidate.category_name:
                    score += 0.2

                if score >= threshold:
                    matches.append({'post': candidate, 'score': min(score, 1.0)})
                    logging.info(f"Found match: {candidate.item_name} with score {score}")

            return sorted(matches, key=lambda x: x['score'], reverse=True)
        except Exception as e:
            logging.error(f"Error finding matches: {e}")
            return []

    def create_match_notification(self, user_id, match_post, original_post, score):
        try:
            # Check if notification already exists
            existing = Notification.query.filter_by(
                user_id=user_id,
                link=f"/posts/post/{match_post.id}"
            ).first()

            if not existing:
                notification = Notification(
                    user_id=user_id,
                    title="Potential Match Found!",
                    message=f"We found a {score:.0%} match for your {original_post.type} item '{original_post.item_name}'",
                    link=f"/posts/post/{match_post.id}",
                    is_read=False
                )
                db.session.add(notification)
                db.session.commit()
                logging.info(f"Created notification for user {user_id}")

        except Exception as e:
            logging.error(f"Error creating notification: {e}")
            db.session.rollback()
