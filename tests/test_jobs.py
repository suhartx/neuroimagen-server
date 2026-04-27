def test_create_job_and_complete_inline(client):
    upload = client.post(
        "/studies/upload",
        files={"file": ("brain.nii.gz", b"dummy-mri", "application/gzip")},
        data={"enqueue_processing": "false"},
    )
    assert upload.status_code == 201
    study_id = upload.json()["study_id"]

    create_job = client.post("/jobs", json={"study_id": study_id, "parameters": {"pipeline": "local"}})
    assert create_job.status_code == 202
    job_id = create_job.json()["job_id"]

    job_state = client.get(f"/jobs/{job_id}")
    assert job_state.status_code == 200
    payload = job_state.json()
    assert payload["status"] == "completed"
    assert payload["result"]["report_path"].endswith("report.pdf")

    result = client.get(f"/jobs/{job_id}/result")
    assert result.status_code == 200

    report = client.get(f"/jobs/{job_id}/report")
    assert report.status_code == 200
    assert report.headers["content-type"] == "application/pdf"
