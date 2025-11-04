from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

def home_view(request):
	return render(request,'home.html')


def about_view(request):
	return render(request,'about.html')


def contact_view(request):
	return render(request,'contact.html')

@login_required(login_url="login")
def animation_view(request):
	if request.method == 'POST':
		try:
			text = request.POST.get('sen')
			#tokenizing the sentence
			text.lower()
			#tokenizing the sentence
			words = word_tokenize(text)

			tagged = nltk.pos_tag(words)
			tense = {}
			tense["future"] = len([word for word in tagged if word[1] == "MD"])
			tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
			tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
			tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])



			#stopwords that will be removed
			stop_words = set(["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've",'off', 'for', "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don', 'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the', 'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have',  'hasn', 'o', "aren't", "you'll", "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself', 'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did', 'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])



			#removing stopwords and applying lemmatizing nlp process to words
			try:
				lr = WordNetLemmatizer()
				use_lemmatizer = True
			except LookupError:
				# If WordNet/omw-1.4 is not available, skip lemmatization
				use_lemmatizer = False
				lr = None
			
			filtered_text = []
			for w,p in zip(words,tagged):
				if w not in stop_words:
					if use_lemmatizer:
						try:
							if p[1]=='VBG' or p[1]=='VBD' or p[1]=='VBZ' or p[1]=='VBN' or p[1]=='NN':
								filtered_text.append(lr.lemmatize(w,pos='v'))
							elif p[1]=='JJ' or p[1]=='JJR' or p[1]=='JJS'or p[1]=='RBR' or p[1]=='RBS':
								filtered_text.append(lr.lemmatize(w,pos='a'))
							else:
								filtered_text.append(lr.lemmatize(w))
						except LookupError:
							# If omw-1.4/wordnet not available at runtime, stop lemmatizing further
							use_lemmatizer = False
							filtered_text.append(w)
					else:
						# Without lemmatizer, just use the word as-is
						filtered_text.append(w)

			#adding the specific word to specify tense
			words = filtered_text
			temp=[]
			for w in words:
				if w=='I':
					temp.append('Me')
				else:
					temp.append(w)
			words = temp
			probable_tense = max(tense,key=tense.get)

			if probable_tense == "past" and tense["past"]>=1:
				temp = ["Before"]
				temp = temp + words
				words = temp
			elif probable_tense == "future" and tense["future"]>=1:
				if "Will" not in words:
						temp = ["Will"]
						temp = temp + words
						words = temp
				else:
					pass
			elif probable_tense == "present":
				if tense["present_continuous"]>=1:
					temp = ["Now"]
					temp = temp + words
					words = temp


			filtered_text = []
			for w in words:
				path = w + ".mp4"
				f = finders.find(path)
				#splitting the word if its animation is not present in database
				if not f:
					for c in w:
						filtered_text.append(c)
				#otherwise animation of word
				else:
					filtered_text.append(w)
			words = filtered_text;


			return render(request,'animation.html',{'words':words,'text':text})
		except LookupError as e:
			# NLTK data is missing
			error_msg = str(e)
			instructions = """
			<h2>NLTK Data Not Found</h2>
			<p>The application requires NLTK data to process text. Please download the required data by running:</p>
			<pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">
cd "C:\\Users\\likit\\OneDrive\\Desktop\\Audio-Speech-To-Sign-Language-Converter-master\\Audio-Speech-To-Sign-Language-Converter-master"
.\\venv\\Scripts\\Activate.ps1
python download_nltk_data.py
			</pre>
			<p>Or manually download using Python:</p>
			<pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet'); nltk.download('omw-1.4')"
			</pre>
			<p>If you continue to have network issues, please check your internet connection and try again.</p>
			"""
			return HttpResponse(instructions, content_type='text/html')
		except Exception as e:
			# Generic error handling
			error_msg = f"An error occurred: {str(e)}"
			return HttpResponse(f"<h2>Error</h2><p>{error_msg}</p>", content_type='text/html')
	else:
		return render(request,'animation.html')




def signup_view(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			# log the user in
			return redirect('animation')
	else:
		form = UserCreationForm()
	return render(request,'signup.html',{'form':form})



def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#log in user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('animation')
	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect("home")


def summarizer_view(request):
    return render(request,'summarizer.html')