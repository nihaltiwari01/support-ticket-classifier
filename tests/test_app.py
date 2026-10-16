import app as app_module


def client():
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_predict_returns_category():
    res = client().post("/predict", json={"message": "I was charged twice for my subscription"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["category"] != ""
    assert 0 <= data["confidence"] <= 100


def test_predict_rejects_empty_message():
    res = client().post("/predict", json={"message": "   "})
    assert res.status_code == 400


def test_stats_endpoint_works():
    res = client().get("/stats")
    assert res.status_code == 200
    assert "total" in res.get_json()
