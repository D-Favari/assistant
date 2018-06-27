from gtts import gTTS
import speech_recognition as sr
import os
import webbrowser
import smtplib
import wolframalpha
import wikipedia

def talkToMe(audio):

	print(audio)
	tts = gTTS(text=audio, lang='en')
	tts.save('audio.mp3')
	os.system('audio.mp3')

# receber comandos

def myCommand():

	r = sr.Recognizer()

	with sr.Microphone() as source:
		talkToMe("I'm ready.")
		print("I'm ready")
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration = 1)
		audio = r.listen(source)

	try:
		pesquisa = r.recognize_google(audio).lower()
		print("Voce disse: " + pesquisa + '\n')

	# volta a receber comandos
	except sr.UnknownValueError:
		print("I can't understand you")
		assistant(myCommand())

	return pesquisa

# executar os comandos
def assistant(pesquisa):

	new = 2
	google = "http://google.com/?#q="
	youtube = "https://www.youtube.com/results?search_query="


	if "google" in pesquisa:
		webbrowser.open(google+pesquisa,new=new)
	if "youtube" in pesquisa:
   		webbrowser.open(youtube+pesquisa,new=new)

	if 'email' in pesquisa:
		talkToMe('Who is the recipient?')
		recipient = myCommand()

		if 'myself' in recipient:
			talkToMe('What should I say?')
			content = myCommand()

            #init gmail SMTP
			mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
			mail.ehlo()

            #encrypt session
			mail.starttls()

            #login
			mail.login('user@hotmail.com', 'password')

            #send message
			mail.sendmail('name', 'email@addres', content)

            #end mail connection
			mail.close()
			talkToMe('Email sent.')
		else:
			talkToMe('I don\'t know what you mean!')
	else:
		try:
			# wolframalpha
			app_id = "YPLAHR-U3AWJK9T97"
			client = wolframalpha.Client(app_id)
			res = client.query(pesquisa)
			answer = next(res.results).text
			print(answer)
			talkToMe(answer)
		except:
			# wikipedia
			print(wikipedia.summary(pesquisa))
			talkToMe(wikipedia.summary(pesquisa))

while True:
	assistant(myCommand())
