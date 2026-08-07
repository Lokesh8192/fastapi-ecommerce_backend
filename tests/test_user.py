from fastapi import status


def test_get_profile(
    client,
    auth_headers,
):
    response = client.get(
        "/users/me",
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK
