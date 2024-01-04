## How to run the audio transpiler 

 - install the dependencies `pip install -r requirements.txt` 
 - on MacOS, PyAudio has a system dependency on `portaudio`, so you'll need to install that 
 - `brew install portaudio` 
 - set your openai api key in the terminal or wherever `export OPENAI_API_KEY='yourkey'`
 - `python main.py` 
 - hold "r" and the program will capture whatever audio comes into your computer's selected audio input. 
 - release "r" when done. 
 - if it's all setup correctly, you should see a printed output from openai with the transcript of your audio in the console. 

