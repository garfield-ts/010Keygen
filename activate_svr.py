from flask import Flask
app = Flask(__name__)
 
@app.route('/cgibin/010editor_check_license_9b.php')
def hello():
    print("Handled")
    #return "valid"
    return "<ss>valid</ss>"
 
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
