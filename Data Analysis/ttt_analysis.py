import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

### GET DATA ###

db_link = sqlite3.connect('tictactoe.db')
df = pd.read_sql("SELECT * FROM game_data", db_link)
db_link.close()

### EXPLORE DATA ###

def explore_data():
	print(df.head(1))
	print(df.isnull().sum())
	print(df.describe())

### VISUALIZE DATA ###

def outcome_distribution():
	plt.figure(figsize=(8,5))
	sns.countplot(data=df, x='outcome', order=df['outcome'].value_counts().index, palette="viridis")
	plt.title('Distribution of Game Outcomes')
	plt.ylabel('Number of Games')
	plt.xlabel('Outcome')
	plt.show()


def common_board_states():
	top_board_states = df['board_state'].value_counts().head(10).index
	plt.figure(figsize=(12,6))
	sns.countplot(data=df[df['board_state'].isin(top_board_states)], x='board_state', order=top_board_states, palette="viridis")
	plt.title('Top 10 Most Common Board States')
	plt.ylabel('Frequency')
	plt.xlabel('Board State')
	plt.xticks(rotation=45)
	plt.show()


def moves_distribution():
	plt.figure(figsize=(8,5))
	sns.countplot(data=df, x='move_made', order=df['move_made'].value_counts().index, palette="viridis")
	plt.title('Distribution of Moves Made')
	plt.ylabel('Number of Moves')
	plt.xlabel('Move Made')
	plt.show()

def outcomes_vs_moves():
	outcome_move_ct = pd.crosstab(df['move_made'], df['outcome'])
	plt.figure(figsize=(10,6))
	sns.heatmap(outcome_move_ct, annot=True, cmap='viridis', fmt="d")
	plt.title('Heatmap of Outcomes vs. Moves Made')
	plt.show()

def correlation():
	corr = df.corr()
	sns.heatmap(corr, annot=True, cmap='coolwarm')
	plt.title('Correlation Heatmap')
	plt.show()

def dist_first_move():
	first_moves = df[df['move_order'] == 1]['move_made']
	sns.countplot(first_moves)
	plt.title('Distribution of First Moves')
	plt.show()

def dist_initial_state():
	initial_states = df[df['move_order'] == 2].groupby('board_state')['outcome'].value_counts().unstack().fillna(0)
	initial_states.plot(kind='bar', stacked=True)
	plt.title('Outcomes Based on Initial Board States')
	plt.show()


def analyze():
	outcome_distribution()
	moves_distribution()
	common_board_states()
	outcomes_vs_moves()
	correlation()
	dist_first_move()
	dist_initial_state()

analyze()