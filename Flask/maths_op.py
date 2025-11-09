from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_post():
    try:
        data = request.get_json()
        operation = data.get('operation')
        a = float(data.get('a'))
        b = float(data.get('b'))
        
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                return jsonify({'error': 'Division by zero is not allowed'}), 400
            result = a / b
        else:
            return jsonify({'error': 'Invalid operation. Supported: add, subtract, multiply, divide'}), 400
        
        return jsonify({'result': result})
    
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input. Ensure JSON has "operation", "a", and "b" as numbers.'}), 400

@app.route('/calculate', methods=['GET'])
def calculate_get():
    try:
        operation = request.args.get('operation')
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                return jsonify({'error': 'Division by zero is not allowed'}), 400
            result = a / b
        else:
            return jsonify({'error': 'Invalid operation. Supported: add, subtract, multiply, divide'}), 400
        
        return jsonify({'result': result})
    
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid input. Ensure query params "operation", "a", and "b" are provided with "a" and "b" as numbers.'}), 400

if __name__ == '__main__':
    app.run(debug=True)