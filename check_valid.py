def validate_associations(existing_associations, new_associations):
    valid_associations = []
    invalid_associations = []
    
    company_role_counts = {}
    contact_role_counts = {}

    for assoc in existing_associations:
        company_id, contact_id, role = assoc['companyId'], assoc['contactId'], assoc['role']
        company_role_counts.setdefault((company_id, role), set()).add(contact_id)
        contact_role_counts.setdefault((contact_id, company_id), set()).add(role)
    
    new_role_counts = {}
    new_contact_role_counts = {}
    
    for assoc in new_associations:
        company_id, contact_id, role = assoc['companyId'], assoc['contactId'], assoc['role']
        new_role_counts[(company_id, role)] = new_role_counts.get((company_id, role), 0) + 1
        if (contact_id, company_id) not in new_contact_role_counts:
            new_contact_role_counts[(contact_id, company_id)] = set()
        new_contact_role_counts[(contact_id, company_id)].add(role)

    for assoc in new_associations:
        company_id, contact_id, role = assoc['companyId'], assoc['contactId'], assoc['role']

        if contact_id in company_role_counts.get((company_id, role), set()):
            assoc['failureReason'] = "ALREADY_EXISTS"
            invalid_associations.append(assoc)
            continue

        existing_role_count = len(company_role_counts.get((company_id, role), set()))
        existing_contact_role_count = len(contact_role_counts.get((contact_id, company_id), set()))
        
        if existing_role_count + new_role_counts[(company_id, role)] > 5:
            assoc['failureReason'] = "WOULD_EXCEED_LIMIT"
            invalid_associations.append(assoc)
            continue

        total_new_roles_for_contact = len(new_contact_role_counts.get((contact_id, company_id), set()))
        if existing_contact_role_count + total_new_roles_for_contact > 2:
            assoc['failureReason'] = "WOULD_EXCEED_LIMIT"
            invalid_associations.append(assoc)
            continue

        valid_associations.append(assoc)
        
        company_role_counts.setdefault((company_id, role), set()).add(contact_id)
        contact_role_counts.setdefault((contact_id, company_id), set()).add(role)
    
    total_processed = len(valid_associations) + len(invalid_associations)
    assert total_processed == len(new_associations), \
        f"Mismatch in total associations. Expected {len(new_associations)}, but got {total_processed}."

    return valid_associations, invalid_associations
