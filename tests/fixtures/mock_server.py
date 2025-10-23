import json

import responses

BASE_URL = "https://localhost:8000/api/v1"


def setup_mock_server():
    responses.add(
        responses.POST,
        f"{BASE_URL}/users",
        body=json.dumps({
            "email": "test@example.com",
            "username": "testuser",
            "password": "Password123!",
            "confirmPassword": "Password123!",
            "firstName": "Test",
            "lastName": "User",
            "path": "/test",
            "enabled": True,
        }),
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                "created": "2021-10-18T08:47:54.219531Z",
                "updated": "2021-10-18T08:47:54.219531Z",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "tenantID": "4atcicnisg",
                "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                "email": "tom@example.com",
                "enabled": True,
                "firstName": "Tom",
                "lastName": "Jasper",
                "username": "tom",
                "path": "/org1",
                "metadata": {"language": "uk", "age": 23},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=201,
        content_type="application/json",
        match_querystring=True,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                    "created": "2021-10-18T08:47:54.219531Z",
                    "updated": "2021-10-18T08:47:54.219531Z",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                    "tenantID": "4atcicnisg",
                    "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                    "email": "tom@example.com",
                    "enabled": True,
                    "firstName": "Tom",
                    "lastName": "Jasper",
                    "username": "tom",
                    "path": "/org1",
                    "metadata": {"language": "uk", "age": 23},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/paths",
        json={"data": ["/org1", "/org2"]},
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/users/delete", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                "created": "2021-10-18T08:47:54.219531Z",
                "updated": "2021-10-18T08:47:54.219531Z",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "tenantID": "4atcicnisg",
                "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                "email": "tom@example.com",
                "enabled": True,
                "firstName": "Tom",
                "lastName": "Jasper",
                "username": "tom",
                "path": "/org1",
                "metadata": {"language": "uk", "age": 23},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.PATCH, f"{BASE_URL}/users/me", status=204)

    responses.add(responses.DELETE, f"{BASE_URL}/users/me", status=204)

    responses.add(responses.PUT, f"{BASE_URL}/users/me/metadata", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me/irn",
        json={"data": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom"},
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/users/me/password/change", status=204)

    responses.add(responses.POST, f"{BASE_URL}/users/me/password/reset", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me/groups",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "tenantID": "4atcicnisg",
                    "displayName": "Java",
                    "name": "java",
                    "path": "/dev",
                    "metadata": {"location": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                    "created": "2021-10-18T11:08:09.4919Z",
                    "updated": "2021-10-18T11:08:09.4919Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/users/me/groups/add", status=200)

    responses.add(responses.POST, f"{BASE_URL}/users/me/groups/remove", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me/policies/eligible",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.PUT, f"{BASE_URL}/users/me/policies/attach", status=204)

    responses.add(responses.POST, f"{BASE_URL}/users/me/policies/detach", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/me/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp1c2VyL2plcnJ5",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "name": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "description": "Individual resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Jerry everything on Tom user",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:47g5l2ijc0::user/jerry"],
                        "effect": "allow",
                    }
                ],
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.PUT, f"{BASE_URL}/users/me/policy", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                "created": "2021-10-18T08:47:54.219531Z",
                "updated": "2021-10-18T08:47:54.219531Z",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "tenantID": "4atcicnisg",
                "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                "email": "tom@example.com",
                "enabled": True,
                "firstName": "Tom",
                "lastName": "Jasper",
                "username": "tom",
                "path": "/org1",
                "metadata": {"language": "uk", "age": 23},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PATCH,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/metadata",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/password/change",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/password/reset",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/password/forgot",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/groups",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "tenantID": "4atcicnisg",
                    "displayName": "Java",
                    "name": "java",
                    "path": "/dev",
                    "metadata": {"location": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                    "created": "2021-10-18T11:08:09.4919Z",
                    "updated": "2021-10-18T11:08:09.4919Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/groups/add",
        status=200,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/groups/remove",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/policies/eligible",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/policies/attach",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9y/policies/detach",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp1c2VyL2plcnJ5",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "name": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                "description": "Individual resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Jerry everything on Tom user",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:47g5l2ijc0::user/jerry"],
                        "effect": "allow",
                    }
                ],
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/users/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/policy",
        status=204,
    )

    # Groups
    responses.add(
        responses.POST,
        f"{BASE_URL}/groups",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                "tenantID": "4atcicnisg",
                "displayName": "Java",
                "name": "java",
                "path": "/dev",
                "metadata": {"location": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                "created": "2021-10-18T11:08:09.4919Z",
                "updated": "2021-10-18T11:08:09.4919Z",
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "tenantID": "4atcicnisg",
                    "displayName": "Java",
                    "name": "java",
                    "path": "/dev",
                    "metadata": {"location": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                    "created": "2021-10-18T11:08:09.4919Z",
                    "updated": "2021-10-18T11:08:09.4919Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/groups/delete", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                "tenantID": "4atcicnisg",
                "displayName": "Java",
                "name": "java",
                "path": "/dev",
                "metadata": {"location": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                "created": "2021-10-18T11:08:09.4919Z",
                "updated": "2021-10-18T11:08:09.4919Z",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/metadata",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/members",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                    "created": "2021-10-18T08:47:54.219531Z",
                    "updated": "2021-10-18T08:47:54.219531Z",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                    "tenantID": "4atcicnisg",
                    "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                    "email": "tom@example.com",
                    "enabled": True,
                    "firstName": "Tom",
                    "lastName": "Jasper",
                    "username": "tom",
                    "path": "/org1",
                    "metadata": {"language": "uk", "age": 23},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/members/eligible",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t",
                    "created": "2021-10-18T08:47:54.219531Z",
                    "updated": "2021-10-18T08:47:54.219531Z",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::user/org1/tom",
                    "tenantID": "4atcicnisg",
                    "authID": "68a8372d-cc0a-4a42-8a56-099ac466e0bd",
                    "email": "tom@example.com",
                    "enabled": True,
                    "firstName": "Tom",
                    "lastName": "Jasper",
                    "username": "tom",
                    "path": "/org1",
                    "metadata": {"language": "uk", "age": 23},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/members/add",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/members/remove",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policies/eligible",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policies/attach",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policies/detach",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXY=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev",
                "name": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev",
                "description": "Individual resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Tom everything on dev group",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/tom"],
                        "effect": "allow",
                    }
                ],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/groups/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==/policy",
        status=204,
    )

    # Resources
    responses.add(
        responses.POST,
        f"{BASE_URL}/resources",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "created": "2022-10-25T22:22:17.390631+03:00",
                "updated": "2022-10-25T22:22:17.390631+03:00",
                "tenantID": "4atcicnisg",
                "application": "myapp",
                "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "displayName": "Thermostat",
                "path": "/dev",
                "resourceType": "device",
                "enabled": True,
                "description": "Resource description",
                "metadata": {"temperature": 10, "city": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/resources",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                    "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "created": "2022-10-25T22:22:17.390631+03:00",
                    "updated": "2022-10-25T22:22:17.390631+03:00",
                    "tenantID": "4atcicnisg",
                    "application": "myapp",
                    "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                    "displayName": "Thermostat",
                    "path": "/dev",
                    "resourceType": "device",
                    "enabled": True,
                    "description": "Resource description",
                    "metadata": {"temperature": 10, "city": "Kyiv"},
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 100,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/resources/delete", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "created": "2022-10-25T22:22:17.390631+03:00",
                "updated": "2022-10-25T22:22:17.390631+03:00",
                "tenantID": "4atcicnisg",
                "application": "myapp",
                "name": "7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "displayName": "Thermostat",
                "path": "/dev",
                "resourceType": "device",
                "enabled": True,
                "description": "Resource description",
                "metadata": {"temperature": 10, "city": "Kyiv"},
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PATCH,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=",
                "irn": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "name": "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "description": "Individual resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Jerry everything on the resource",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                        "effect": "allow",
                    }
                ],
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=/policy",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/resources/aXJuOnJjNzNkYmg3cTA6bXlhcHA6NGF0Y2ljbmlzZzo6ZGV2aWNlL2Rldi83ZTFlZGFkNS03ODQxLTRkMzgtYmRmMS1iZGM1NzViMGU5ODk=/pools/eligible",
        json={
            "data": [
                "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg==",
                "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2Q=",
            ],
            "count": 2,
            "page": 1,
            "pageSize": 100,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/resources/evaluate",
        json=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/tom", "irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
        status=200,
        content_type="application/json",
    )

    # Evaluate
    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate",
        json=["irn:rc73dbh7q0:iamcore:4atcicnisg::user/tom", "irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate/resources",
        json={
            "data": [
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/fcdd2d70-e4fc-4762-965c-ffc829a19b0a",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/1ff6f1ae-5712-11ed-9b6a-0242ac120002",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/2644ce6e-5712-11ed-9b6a-0242ac120002",
            ],
            "count": 4,
            "page": 1,
            "pageSize": 100,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate/actions",
        json={
            "irn:rc73dbh7q0:iamcore:4atcicnisg::group/*": ["iamcore:group:read"],
            "irn:rc73dbh7q0:myapp:4atcicnisg::user/tom": ["iamcore:user:read"],
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate/irns/actions",
        json={
            "iamcore:group:read": {
                "allowed": [
                    "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev1/*",
                    "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev2",
                ],
                "denied": ["irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev1/java"],
            },
            "iamcore:group:update": {"allowed": [], "denied": ["irn:rc73dbh7q0:iamcore:4atcicnisg::group/*"]},
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate/debug/resources",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "decision": "deny",
                    "actions": [
                        {
                            "action": "iamcore:group:read",
                            "decision": "deny",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-java-group-read",
                                "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-on-java-group",
                            ],
                            "denyPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/deny-java-group-read-for-jerry"
                            ],
                        },
                        {
                            "action": "iamcore:group:update",
                            "decision": "allow",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-java-group-update",
                                "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-on-java-group",
                            ],
                        },
                    ],
                },
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYva290bGlu",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/kotlin",
                    "decision": "allow",
                    "actions": [
                        {
                            "action": "iamcore:group:read",
                            "decision": "allow",
                            "allowPolicies": ["irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-kotlin-group-read"],
                        },
                        {
                            "action": "iamcore:group:update",
                            "decision": "allow",
                            "allowPolicies": ["irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-kotlin-group-update"],
                        },
                    ],
                },
            ],
            "evaluationTimeMillis": 43,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/evaluate/debug/resources/type",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYvamF2YQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/java",
                    "decision": "deny",
                    "actions": [
                        {
                            "action": "iamcore:group:read",
                            "decision": "deny",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctamF2YS1ncm91cC1yZWFk",
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctYWxsLW9uLWphdmEtZ3JvdXA=",
                            ],
                            "denyPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvZGVueS1qYXZhLWdyb3VwLXJlYWQtZm9yLWplcnJ5"
                            ],
                        },
                        {
                            "action": "iamcore:group:update",
                            "decision": "allow",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctamF2YS1ncm91cC11cGRhdGU=",
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctYWxsLW9uLWphdmEtZ3JvdXA=",
                            ],
                        },
                    ],
                },
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpncm91cC9kZXYva290bGlu",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::group/dev/kotlin",
                    "decision": "allow",
                    "actions": [
                        {
                            "action": "iamcore:group:read",
                            "decision": "allow",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctamF2YS1ncm91cC1yZWFk"
                            ],
                        },
                        {
                            "action": "iamcore:group:update",
                            "decision": "allow",
                            "allowPolicies": [
                                "irn:rc73dbh7q0:iamcore:4atcicnisnOjpwb2xpY3kvYWxsb3ctamF2YS1ncm91cC11cGRhdGU="
                            ],
                        },
                    ],
                },
            ],
            "evaluationTimeMillis": 43,
            "count": 2,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    # Policies
    responses.add(
        responses.POST,
        f"{BASE_URL}/policies",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                "name": "allow-all-actions-on-jerry",
                "description": "Allow all actions on Jerry",
                "type": "identity",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "actions": ["iamcore:user:*"],
                        "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                        "effect": "allow",
                        "description": "Allow all actions on Jerry",
                    }
                ],
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/policies/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                "name": "allow-all-actions-on-jerry",
                "description": "Allow all actions on Jerry",
                "type": "identity",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "actions": ["iamcore:user:*"],
                        "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                        "effect": "allow",
                        "description": "Allow all actions on Jerry",
                    }
                ],
                "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/policies/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/policies/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/policies/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=/principals",
        json={
            "data": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry", "irn:rc73dbh7q0:iamcore:4atcicnisg::user/joseph"]
        },
        status=200,
        content_type="application/json",
    )

    # Tenants
    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/issuers",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ==",
                    "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::issuer/iamcore",
                    "name": "iamcore",
                    "type": "iamcore",
                    "url": "https://iamcore.io/auth",
                    "loginURL": "https://iamcore.io/login",
                    "clientID": "a04583ab-cdc5-4991-ad1c-1e5555adea7e",
                }
            ]
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/tenants/issuer-types/iamcore",
        json={
            "data": {
                "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                "tenantID": "47g5l2ijc0",
                "name": "my-tenant",
                "displayName": "My tenant",
                "loginTheme": "My theme",
                "issuerType": "iamcore",
                "userMetadataUiSchema": {"key": "val"},
                "groupMetadataUiSchema": {"key": "val"},
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants",
        json={
            "data": [
                {
                    "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                    "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                    "tenantID": "47g5l2ijc0",
                    "name": "my-tenant",
                    "displayName": "My tenant",
                    "loginTheme": "My theme",
                    "issuerType": "iamcore",
                    "userMetadataUiSchema": {"key": "val"},
                    "groupMetadataUiSchema": {"key": "val"},
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/a3JuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
        json={
            "data": {
                "resourceID": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
                "irn": "irn:rc73dbh7q0:iamcore:47g5l2ijc0::tenant/47g5l2ijc0",
                "tenantID": "47g5l2ijc0",
                "name": "my-tenant",
                "displayName": "My tenant",
                "loginTheme": "My theme",
                "issuerType": "iamcore",
                "userMetadataUiSchema": {"key": "val"},
                "groupMetadataUiSchema": {"key": "val"},
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/tenants/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/tenants/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==",
        status=204,
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/tenants/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==/issuer-types/iamcore/issuers",
        status=201,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==/issuer-types/iamcore/issuers/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ==/settings",
        json={"data": {"redirectURIs": ["*", "http://localhost:4200"]}},
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/tenants/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjp0ZW5hbnQvNDdnNWwyaWpjMA==/issuer-types/iamcore/issuers/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0N2c1bDJpamMwOjppc3N1ZXIvaWFtY29yZQ==/settings",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/47g5l2ijc0/email-templates",
        json={
            "data": [
                {
                    "type": "reset-password",
                    "subject": "Reset password",
                    "template": "<!DOCTYPE html><html><body><p><a href={{link}}>Link to reset password</a><p> This link will expire within {{linkExpirationTime}}.</body></html>",
                },
                {
                    "type": "verify-email",
                    "template": "<!DOCTYPE html><html><body><p><a href={{link}}>Link to verify your e-mail address</a><p>This link is valid for {{linkExpirationTime}}.</body></html>",
                },
            ]
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.PUT, f"{BASE_URL}/tenants/47g5l2ijc0/email-templates/reset-password", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/47g5l2ijc0/email-templates/reset-password",
        json={
            "data": {
                "type": "reset-password",
                "subject": "Reset password",
                "template": "<!DOCTYPE html><html><body><p><a href={{link}}>Link to reset password</a><p> This link will expire within {{linkExpirationTime}}.</body></html>",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/tenants/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp0ZW5hbnQvNGF0Y2ljbmlzZw==",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::tenant/4atcicnisg",
                "name": "irn:rc73dbh7q0:iamcore:4atcicnisg::tenant/4atcicnisg",
                "description": "Individual resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Tom everything on tenant",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/tom"],
                        "effect": "allow",
                    }
                ],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.PUT, f"{BASE_URL}/tenants/policy", status=204)

    # Accounts
    responses.add(responses.POST, f"{BASE_URL}/accounts", status=201)

    responses.add(
        responses.GET,
        f"{BASE_URL}/accounts/aXJuOjRhdGNpY25pc2c6aWFtY29yZTo6OmFjY291bnQvNGF0Y2ljbmlzZw==/profile",
        json={
            "data": {
                "accountType": "company",
                "firstName": "Tom",
                "lastName": "Jasper",
                "companyName": "Acme Inc.",
                "jobCategory": "Software Engineer",
                "industry": "Technology",
                "country": "United States",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/accounts/aXJuOjRhdGNpY25pc2c6aWFtY29yZTo6OmFjY291bnQvNGF0Y2ljbmlzZw==/profile",
        status=204,
    )

    # Applications
    responses.add(
        responses.POST,
        f"{BASE_URL}/applications",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "myapp",
                "displayName": "My app name",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                    "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                    "name": "myapp",
                    "displayName": "My app name",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "myapp",
                "displayName": "My app name",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT, f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw", status=204
    )

    responses.add(
        responses.POST,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/resource-types",
        status=201,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/resource-types",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                    "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                    "type": "document",
                    "description": "Representation of the 'document' resource type",
                    "actionPrefix": "document",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                    "operations": ["sign", "export"],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/resource-types/aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
                "irn": "irn:rc73dbh7q0:myapp:::resource-type/document",
                "type": "document",
                "description": "Representation of the 'document' resource type",
                "actionPrefix": "document",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
                "operations": ["sign", "export"],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/resource-types/aXJuOnJjNzNkYmg3cTA6bXlhcHA6OjpyZXNvdXJjZS10eXBlL2RvY3VtZW50",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policy",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw",
                "irn": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "name": "irn:rc73dbh7q0:iamcore:::application/myapp",
                "description": "Resource policy",
                "type": "resource",
                "origin": "api",
                "version": "1.0.0",
                "statements": [
                    {
                        "description": "Allow Tom everything on application",
                        "actions": ["*"],
                        "principals": ["irn:rc73dbh7q0:iamcore:root::user/tom"],
                        "effect": "allow",
                    }
                ],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policy",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policies/attach",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policies/detach",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/applications/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo6OmFwcGxpY2F0aW9uL215YXBw/policies/eligible",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    # Pools
    responses.add(
        responses.POST,
        f"{BASE_URL}/pools",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::pool/prod/admin",
                "name": "admin",
                "resources": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL3RvbQ=="],
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/pools",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::pool/prod/admin",
                    "name": "admin",
                    "resources": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL3RvbQ=="],
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(responses.POST, f"{BASE_URL}/pools/delete", status=204)

    responses.add(
        responses.GET,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
        json={
            "data": {
                "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
                "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::pool/prod/admin",
                "name": "admin",
                "resources": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL3RvbQ=="],
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
        status=204,
    )

    responses.add(
        responses.DELETE,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=/attach",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=/detach",
        status=204,
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/pools/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL3Byb2QvYWRtaW4=/resources/eligible",
        json={
            "data": [
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/fcdd2d70-e4fc-4762-965c-ffc829a19b0a",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/dev/7e1edad5-7841-4d38-bdf1-bdc575b0e989",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/1ff6f1ae-5712-11ed-9b6a-0242ac120002",
                "irn:rc73dbh7q0:myapp:4atcicnisg::device/2644ce6e-5712-11ed-9b6a-0242ac120002",
            ],
            "count": 4,
            "page": 1,
            "pageSize": 100,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/pools/attach/resource/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL2Jlbg==",
        status=204,
    )

    # Anonymous
    responses.add(responses.PUT, f"{BASE_URL}/anonymous/policies/attach", status=204)

    responses.add(responses.POST, f"{BASE_URL}/anonymous/policies/detach", status=204)

    # API Keys
    responses.add(
        responses.POST,
        f"{BASE_URL}/principals/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/api-keys",
        json={
            "data": {
                "apiKey": "2W9Xv6Ae7y0nHf8Mb1JdKc5Tl4sZgIzNtEjPuSqOxDhYi3LrpQmGkFVbCh94ygh6",
                "state": "active",
                "lastUsed": "2021-10-19T17:57:31.14492667Z",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=201,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/principals/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/api-keys",
        json={
            "data": [
                {
                    "apiKey": "5D8g3hFbK7YpZ9cE2qXsW6vRoA1TnI4uM0ljOJNtViUmkQzx989gSkadh23hga14",
                    "state": "active",
                    "lastUsed": "2021-10-19T17:57:31.14492667Z",
                    "created": "2021-10-18T12:27:15.55267632Z",
                    "updated": "2021-10-18T12:27:15.55267632Z",
                }
            ],
            "count": 1,
            "page": 1,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.GET,
        f"{BASE_URL}/principals/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/api-keys/2W9Xv6Ae7y0nHf8Mb1JdKc5Tl4sZgIzNtEjPuSqOxDhYi3LrpQmGkFVbCh94ygh6",
        json={
            "data": {
                "apiKey": "2W9Xv6Ae7y0nHf8Mb1JdKc5Tl4sZgIzNtEjPuSqOxDhYi3LrpQmGkFVbCh94ygh6",
                "state": "active",
                "lastUsed": "2021-10-19T17:57:31.14492667Z",
                "created": "2021-10-18T12:27:15.55267632Z",
                "updated": "2021-10-18T12:27:15.55267632Z",
            }
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/principals/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjp1c2VyL29yZzEvdG9t/api-keys/2W9Xv6Ae7y0nHf8Mb1JdKc5Tl4sZgIzNtEjPuSqOxDhYi3LrpQmGkFVbCh94ygh6",
        status=204,
    )

    # Roles
    responses.add(
        responses.GET,
        f"{BASE_URL}/roles/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg==/policies",
        json={
            "data": [
                {
                    "id": "aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb2xpY3kvYWxsb3ctYWxsLWFjdGlvbnMtb24tamVycnk=",
                    "irn": "irn:rc73dbh7q0:iamcore:4atcicnisg::policy/allow-all-actions-on-jerry",
                    "name": "allow-all-actions-on-jerry",
                    "description": "Allow all actions on Jerry",
                    "type": "identity",
                    "origin": "api",
                    "version": "1.0.0",
                    "statements": [
                        {
                            "description": "Allow all actions on Jerry",
                            "actions": ["iamcore:user:*"],
                            "resources": ["irn:rc73dbh7q0:iamcore:4atcicnisg::user/jerry"],
                            "effect": "allow",
                        }
                    ],
                    "poolIDs": ["aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg=="],
                }
            ],
            "count": 1,
            "page": 0,
            "pageSize": 10,
        },
        status=200,
        content_type="application/json",
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/roles/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg==/policies/attach",
        status=204,
    )

    responses.add(
        responses.PUT,
        f"{BASE_URL}/roles/aXJuOnJjNzNkYmg3cTA6aWFtY29yZTo0YXRjaWNuaXNnOjpwb29sL2Rldg==/policies/detach",
        status=204,
    )
