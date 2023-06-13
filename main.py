import difflib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk.download('punkt')


questions_and_answers = [
		{
			"question": "¿What is Donorbox?",
			"answer": "Donorbox is an online fundraising platform that allows nonprofit organizations and individuals to create custom donation pages and receive fast and secure donations."
		},
		{
			"question": "¿How can I create a donation page on Donorbox?",
			"answer": "To create a donation page on Donorbox, simply sign up on the Donorbox website and follow the steps to set up your account. You'll then be able to customize your donation page with content, images, and settings like donation frequency, suggested amounts, and more."
		},
		{
			"question": "¿What payment methods are accepted at Donorbox?",
			"answer": "Donorbox supports various payment methods, including credit and debit card payments through major providers such as Visa, Mastercard, and American Express. Payments can also be accepted through popular online payment services such as PayPal and Apple Pay."
		},
		{
			"question": "¿Is it safe to make donations through Donorbox?",
			"answer": "Yes, Donorbox prioritizes the safety of donations. They use SSL encryption to protect donor data and comply with PCI-DSS security standards. Additionally, donors have the option to donate anonymously if they wish."
		},
		{
			"question": "¿How can I track and manage the donations received?",
			"answer": "Donorbox provides an intuitive administration interface that allows you to track and manage received donations. You can view detailed reports, export data, send automatic donation receipts via email, and securely manage donor information."
		},
		{
			"question": "¿Is there a fee for using Donorbox?",
			"answer": "Donorbox applies a processing fee of 1.5% plus 30 cents for each donation made through the platform. This covers the costs of payment processing and related services. There are no monthly fees or hidden costs."
		},
		{
			"question": "¿Can I integrate Donorbox with my website or email platform?",
			"answer": "Yes, Donorbox offers easy-to-use integrations with popular platforms, including WordPress, Wix, Squarespace, and more. You can also integrate Donorbox with email marketing tools like Mailchimp or Constant Contact to manage your subscriber lists and send emails to donors."
		},
		{
			"question": "¿Can I customize and design my donation page on Donorbox?",
			"answer": "Yes, Donorbox offers customization options so you can adapt the design of your donation page to the image of your organization. You can change colors, add your logo, insert images, and adjust the arrangement of elements on the page."
		},
		{
			"question": "¿Can I set up different donation options, such as one-time and recurring donations?",
			"answer": "Yes, Donorbox allows you to set up one-time and recurring donation options. Donors can choose to make a one-time donation or set up a recurring donation at customizable intervals, such as monthly, quarterly, or yearly."
		},
		{
			"question": "¿Does Donorbox provide tools to send donation receipts to donors?",
			"answer": "Yes, Donorbox automatically generates donation receipts for donors and sends them via email. You can customize the content and appearance of these receipts to suit your organization."
		},
		{
			"question": "¿Can I access reports and analysis on the donations received?",
			"answer": "Yes, Donorbox offers complete reports and analysis on the donations received. You can get data such as the total collected, the number of donors, donation averages and more. These reports will help you evaluate the performance of your fundraising campaign."
		},
		{
			"question": "¿Does Donorbox offer campaign tracking and fundraising goals?",
			"answer": "Yes, Donorbox allows you"
		}
	]


# preprocess_text: Process the text to remove stopwords and punctuation marks.
# Input: text
# Output: text without stopwords and punctuation marks
# Example: preprocess_text("I have reports") -> "have reports"words and punctuation marks.
def preprocess_text(text): 
    tokens = word_tokenize(text.lower()) # Tokenize and lowercase

    # Delete the stopwords and punctuation marks
    stop_words = set(stopwords.words('english')) # Get the stopwords for English
    tokens = [token for token in tokens if token.isalnum() and token not in stop_words]
    return ' '.join(tokens)

def find_answer(question):
    processed_question = preprocess_text(question)

    best_matches = difflib.get_close_matches(processed_question, [preprocess_text(q["question"]) for q in questions_and_answers], n=1, cutoff=0.6)
    if best_matches:
        matched_question = best_matches[0]
        for qr in questions_and_answers:
            if preprocess_text(qr["question"]) == matched_question:
                proximity = difflib.SequenceMatcher(None, processed_question, matched_question).ratio()
                print("Proximity:", proximity)
                return qr["answer"]
    return "sorry, I don't understand your question"

print(find_answer("provide tools to send donation"))
