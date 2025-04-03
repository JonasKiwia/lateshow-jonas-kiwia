import csv
from app import create_app
from models import db, Episode, Guest, Appearance

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    episodes = {}
    guests = {}
    
    episode_counter = 1

    with open('seed.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract the episode date from the 'Show' column.
            show_date = row['Show'].strip()  # e.g., "1/11/99"
            
            # Use the show date as a key to ensure each episode is created only once.
            if show_date not in episodes:
                # Create a new Episode. Here, we assign a sequential number.
                ep = Episode(date=show_date, number=episode_counter)
                db.session.add(ep)
                db.session.flush()  # Flush to get the episode ID immediately.
                episodes[show_date] = ep
                episode_counter += 1
            else:
                ep = episodes[show_date]

            # Extract guest details.
            guest_name = row['Raw_Guest_List'].strip()
            guest_occ = row['GoogleKnowlege_Occupation'].strip()
            
            # Create a unique Guest record if not already added.
            if guest_name not in guests:
                guest = Guest(name=guest_name, occupation=guest_occ)
                db.session.add(guest)
                db.session.flush()  # Flush to get the guest ID.
                guests[guest_name] = guest
            else:
                guest = guests[guest_name]

            # Create an Appearance for this episode and guest.
            # Since the CSV doesn't provide a rating, we assign a default rating of 5.
            appearance = Appearance(rating=5, episode_id=ep.id, guest_id=guest.id)
            db.session.add(appearance)

    # Commit all changes.
    db.session.commit()

    print("Database seeded successfully from CSV!")
