import json


def read_policy(filepath):
    with open(filepath, 'r') as policy:
        return json.load(policy)


def get_topic(policy):
    for statement in policy["Statement"]:
        if "iot:Publish" in statement["Action"] and statement["Effect"] == "Allow":
            for resource in statement["Resource"]:
                if "${arn}topic/$aws" not in resource:
                    return resource


def shorten_topic(topic_string):
    return topic_string.replace("${arn}topic/", "").replace("${clientId}", "")
