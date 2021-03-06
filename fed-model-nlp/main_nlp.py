# Import statements
import nltk
import pandas as pd

# Required modules to do entity analysis
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('treebank')
nltk.download('words')


# Sample speech to read
speech = ['The Federal Reserve is committed to using its full range of tools to support the U.S. economy in this challenging time, thereby promoting its maximum employment and price stability goals.', 'The COVID-19 pandemic is causing tremendous human and economic hardship across the United States and around the world. The pace of the recovery in economic activity and employment has moderated in recent months, with weakness concentrated in the sectors most adversely affected by the pandemic. Weaker demand and earlier declines in oil prices have been holding down consumer price inflation. Overall financial conditions remain accommodative, in part reflecting policy measures to support the economy and the flow of credit to U.S. households and businesses.', 'The path of the economy will depend significantly on the course of the virus, including progress on vaccinations. The ongoing public health crisis continues to weigh on economic activity, employment, and inflation, and poses considerable risks to the economic outlook.', "The Committee seeks to achieve maximum employment and inflation at the rate of 2 percent over the longer run. With inflation running persistently below this longer-run goal, the Committee will aim to achieve inflation moderately above 2 percent for some time so that inflation averages 2 percent over time and longer‑term inflation expectations remain well anchored at 2 percent. The Committee expects to maintain an accommodative stance of monetary policy until these outcomes are achieved. The Committee decided to keep the target range for the federal funds rate at 0 to 1/4 percent and expects it will be appropriate to maintain this target range until labor market conditions have reached levels consistent with the Committee's assessments of maximum employment and inflation has risen to 2 percent and is on track to moderately exceed 2 percent for some time. In addition, the Federal Reserve will continue to increase its holdings of Treasury securities by at least $80 billion per month and of agency mortgage‑backed securities by at least $40 billion per month until substantial further progress has been made toward the Committee's maximum employment and price stability goals. These asset purchases help foster smooth market functioning and accommodative financial conditions, thereby supporting the flow of credit to households and businesses.", "In assessing the appropriate stance of monetary policy, the Committee will continue to monitor the implications of incoming information for the economic outlook. The Committee would be prepared to adjust the stance of monetary policy as appropriate if risks emerge that could impede the attainment of the Committee's goals. The Committee's assessments will take into account a wide range of information, including readings on public health, labor market conditions, inflation pressures and inflation expectations, and financial and international developments.", 'Voting for the monetary policy action were Jerome H. Powell, Chair; John C. Williams, Vice Chair; Thomas I. Barkin; Raphael W. Bostic; Michelle W. Bowman; Lael Brainard; Richard H. Clarida; Mary C. Daly; Charles L. Evans; Randal K. Quarles; and Christopher J. Waller.', 'Implementation Note issued January 27, 2021']


# Make the speech a single string
text = " ".join(speech)

# Main function for the code
# Use data pulled by the fed-communications-gatherer module
def main():

	# # Placeholder code to read from a csv file
	# fed_speeches = pd.read_csv("path to fed speeches.csv")

	tags = nltk.pos_tag(nltk.word_tokenize(text))
	#print(tags)

	# Identify named entities
	print("Here are some of the named entities as seen below.\n\n")
	print(nltk.ne_chunk(tags))
	print("\n\n Here are some of the named entities as seen above.\n\n")

main()