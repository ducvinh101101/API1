from post_api import app
import controller.profile_controller
import controller.model_blood

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)