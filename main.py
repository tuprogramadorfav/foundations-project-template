from great_project import create_app  # noqa: F401

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)