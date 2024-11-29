from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"])
def get_contacts():
    """
    Returns a JSON object with all contacts in the database
    """

    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})

@app.route("/create_contact", methods=["POST"])
def create_contact():
    """
    Creates a new contact in the database

    Expects a JSON object with the following fields:

    - firstName: string
    - lastName: string
    - email: string
    - phone: string

    Returns a JSON object with a success message if the contact was created, or a 400 error if the contact was not created

    """
    
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")
    phone = request.json.get("phone")
    
    if not first_name or not last_name or not email or not phone:
        return (
            jsonify({"message": "All fields are required"}),
            400,
        )
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, phone=phone)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "Contact created"}), 201

@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    """
    Updates an existing contact in the database

    Expects a JSON object with the following fields:

    - firstName: string
    - lastName: string
    - email: string
    - phone: string

    Returns a JSON object with a success message if the contact was updated, or a 404 error if the contact was not found

    """
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)
    contact.phone = data.get("phone", contact.phone)
    
    db.session.commit()
    
    return jsonify({"message": "Contact updated"}), 200

@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    """
    Deletes a contact from the database by the given user_id.

    Parameters:
    - user_id: int, the unique identifier of the contact to be deleted

    Returns:
    A JSON object with a success message if the contact was deleted, or a 404 error if the contact was not found
    """
    contact = Contact.query.get(user_id)
    
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({"message": "Contact deleted"}), 200
        

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    
