from website import create_app #Import from Folder Website create_app Function from init

app = create_app()

if __name__ == '__main__': #if run this file
    app.run(debug=True) #if change rerun the webserver for dev

