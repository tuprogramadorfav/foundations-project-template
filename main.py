from great_project.website import app  # noqa: F401

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
