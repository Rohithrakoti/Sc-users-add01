def invoke(method, url, **kwargs):

    r = requests.request(
        method,
        url,
        headers=HEADERS,
        verify=False,
        **kwargs
    )

    if r.status_code not in [200, 201, 204]:
        print(f"Request Failed : {r.status_code}")
        print(r.text)

    return r
