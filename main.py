import requests
import json
from check_valid import validate_associations

API_KEY = '4f7176289364a7ddc6bde38c346c'

# Given big test case
GET_ENDPOINT = f'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey={API_KEY}'
POST_ENDPOINT = f'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey={API_KEY}'

# Given small test case
# GET_ENDPOINT = f'https://candidate.hubteam.com/candidateTest/v3/problem/test-dataset?userKey={API_KEY}'
# POST_ENDPOINT = f'https://candidate.hubteam.com/candidateTest/v3/problem/test-result?userKey={API_KEY}'

TEST_FILE_NAME = 'test_case_1.json'

def fetch_data(use_test_data=False):
    if use_test_data:
        with open(TEST_FILE_NAME) as json_file:
            data = json.load(json_file)
    else:
        response = requests.get(GET_ENDPOINT)
        response.raise_for_status()
        data = response.json()
    
    return data

def submit_result(valid_associations, invalid_associations):
    payload = {
        "validAssociations": valid_associations,
        "invalidAssociations": invalid_associations
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(POST_ENDPOINT, headers=headers, json=payload)
    return response.status_code, response.text


def main():
    # For using json file test case
    # data = fetch_data(use_test_data=True)
    # existing_associations = data['existingAssociations']
    # new_associations = data['newAssociations']
    # valid_associations, invalid_associations = validate_associations(existing_associations, new_associations)
    # print("Valid Associations:", json.dumps(valid_associations, indent=4))
    # print("Invalid Associations:", json.dumps(invalid_associations, indent=4))

    # For using test data from GET API call
    data = fetch_data(use_test_data=False)
    existing_associations = data['existingAssociations']
    new_associations = data['newAssociations']
    valid_associations, invalid_associations = validate_associations(existing_associations, new_associations)
    status_code, response_text = submit_result(valid_associations, invalid_associations)
    print(f"Submission Status: {status_code}")
    print(f"Response Text: {response_text}")


if __name__ == '__main__':
    main()
