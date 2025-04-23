from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)

# Load data functions
def load_addresses():
    try:
        with open('address.json', 'r') as f:
            return json.load(f)
    except:
        return []

def load_companies():
    try:
        with open('company_data.json', 'r') as f:
            return json.load(f)
    except:
        return []

# Save data functions
def save_addresses(addresses):
    with open('address.json', 'w') as f:
        json.dump(addresses, f, indent=2)

def save_companies(companies):
    with open('company_data.json', 'w') as f:
        json.dump(companies, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/addresses', methods=['GET', 'POST'])
def handle_addresses():
    if request.method == 'GET':
        return jsonify(load_addresses())
    
    if request.method == 'POST':
        addresses = load_addresses()
        new_address = request.json
        # Generate a 4-digit ID
        max_id = max([int(addr['id']) for addr in addresses if addr['id'].isdigit()], default=0)
        new_id = str((max_id + 1) % 10000).zfill(4)
        new_address['id'] = new_id
        new_address['createdOn'] = datetime.utcnow().isoformat() + 'Z'
        new_address['updatedDate'] = new_address['createdOn']
        addresses.append(new_address)
        save_addresses(addresses)
        return jsonify(new_address)

@app.route('/api/companies', methods=['GET', 'POST'])
def handle_companies():
    if request.method == 'GET':
        return jsonify(load_companies())
    
    if request.method == 'POST':
        companies = load_companies()
        new_company = request.json
        # Generate a 4-digit ID
        max_id = max([int(company['id']) for company in companies if company['id'].isdigit()], default=0)
        new_id = str((max_id + 1) % 10000).zfill(4)
        new_company['id'] = new_id
        new_company['createdOn'] = datetime.utcnow().isoformat() + 'Z'
        new_company['updatedDate'] = new_company['createdOn']
        new_company['deleted'] = False
        new_company['selected'] = False
        companies.append(new_company)
        save_companies(companies)
        return jsonify(new_company)

@app.route('/api/companies/<company_id>', methods=['DELETE'])
def delete_company(company_id):
    companies = load_companies()
    companies = [c for c in companies if c['id'] != company_id]
    save_companies(companies)
    return jsonify({'success': True})

@app.route('/api/addresses/<address_id>', methods=['DELETE'])
def delete_address(address_id):
    addresses = load_addresses()
    addresses = [a for a in addresses if a['id'] != address_id]
    save_addresses(addresses)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)