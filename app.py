from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register routes
    @app.route('/')
    def home():
        return {"message": "Welcome to the Late Show API!"}

    # ========== ROUTES ========== #
    # a) GET /episodes
    @app.route('/episodes', methods=['GET'])
    def get_episodes():
        episodes = Episode.query.all()
        return jsonify([e.to_dict() for e in episodes]), 200

    # b) GET /episodes/<int:id>
    @app.route('/episodes/<int:id>', methods=['GET'])
    def get_episode(id):
        episode = Episode.query.get(id)
        if episode:
            # We want to include appearances in the JSON
            # Let’s build a custom dictionary to also show appearances
            ep_dict = episode.to_dict()
            ep_dict["appearances"] = []
            for appearance in episode.appearances:
                # For each appearance, we can use appearance.to_dict()
                # But that includes nested episode again, so we might want
                # a smaller version to avoid deep nesting.
                app_dict = {
                    "id": appearance.id,
                    "rating": appearance.rating,
                    "guest_id": appearance.guest_id,
                    "episode_id": appearance.episode_id,
                    "guest": appearance.guest.to_dict() if appearance.guest else None
                }
                ep_dict["appearances"].append(app_dict)

            return jsonify(ep_dict), 200
        else:
            return jsonify({"error": "Episode not found"}), 404

    # c) GET /guests
    @app.route('/guests', methods=['GET'])
    def get_guests():
        guests = Guest.query.all()
        return jsonify([g.to_dict() for g in guests]), 200

    # d) POST /appearances
    @app.route('/appearances', methods=['POST'])
    def create_appearance():
        data = request.get_json()
        try:
            rating = data["rating"]
            episode_id = data["episode_id"]
            guest_id = data["guest_id"]
        except KeyError:
            return jsonify({"errors": ["Missing required fields"]}), 400

        # Create the appearance
        new_appearance = Appearance(
            rating=rating,
            episode_id=episode_id,
            guest_id=guest_id
        )

        try:
            db.session.add(new_appearance)
            db.session.commit()
        except ValueError as e:
            # This is where rating validations might catch an error
            db.session.rollback()
            return jsonify({"errors": [str(e)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({"errors": ["Something went wrong"]}), 400

        return jsonify(new_appearance.to_dict()), 201

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5555)
