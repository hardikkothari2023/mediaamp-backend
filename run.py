from app import create_app, db

app = create_app()

if __name__ == "__main__":
    print("\n🔹 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods} -> {rule}")

    app.run(debug=True)
