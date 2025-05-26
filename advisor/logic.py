import os
import pandas as pd
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
from dotenv import load_dotenv

load_dotenv()

class FinancialAdvisor:

    embedding_model = None
    client = None
    vector_db = None
    total_profiles = None
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        print("Client Initialized")

        # Load and preprocess data
        csv_path = os.path.join(settings.BASE_DIR, 'advisor', 'data', 'finance_data.csv')
        df = pd.read_csv(csv_path)
        print("Read Finance Data")

        # Fill missing values
        df.fillna("Unknown", inplace=True)

        self.total_profiles = len(df)

        # Text embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Init Text embedding_model")


        # Create embeddings for all profiles
        df['embedding'] = df.apply(self._generate_profile_embedding, axis=1)
        print("create Text embedding_model")

        # Vector database simulation (in production, use Pinecone, Weaviate, etc.)
        self.vector_db = {
            'embeddings': np.array(df['embedding'].tolist()),
            'metadata': df.to_dict('records')
        }
        print("create vector_db")
    
    def _generate_profile_embedding(self, row):
        profile_text = f"""
        Gender: {row['gender']}
        Age: {row['age']}
        Investment Avenues: {row['Investment_Avenues']}
        Primary Investment Factor: {row['Factor']}
        Investment Objective: {row['Objective']}
        Investment Purpose: {row['Purpose']}
        Investment Duration: {row['Duration']}
        Monitoring Frequency: {row['Invest_Monitor']}
        Return Expectation: {row['Expect']}
        Preferred Investment Avenue: {row['Avenue']}
        Savings Objective: {row['What are your savings objectives?']}
        """
        return self.embedding_model.encode(profile_text)
    
    def _find_similar_profiles(self, query_embedding, top_k=3):
        print("Find similar profile")
        similarities = cosine_similarity(
            [query_embedding],
            self.vector_db['embeddings']
        )[0]
        
        top_indices = similarities.argsort()[-top_k:][::-1]
        return [self.vector_db['metadata'][i] for i in top_indices]
    
    def _generate_advice(self, user_profile, similar_profiles):
        print("Generate_advice")
        context = "\n\nSimilar Investor Profiles:\n"
        for i, profile in enumerate(similar_profiles, 1):
            context += f"""
            Profile {i}:
            - Age: {profile['age']}
            - Gender: {profile['gender']}
            - Objective: {profile['Objective']}
            - Preferred Avenue: {profile['Avenue']}
            - Return Expectation: {profile['Expect']}
            - Duration: {profile['Duration']}
            """
        
        prompt = f"""
        You are a financial advisor helping a client with investment decisions.
        Below is the client's profile followed by similar investor profiles from your database.
        
        Client Profile:
        - Age: {user_profile['age']}
        - Gender: {user_profile['gender']}
        - Investment Objective: {user_profile['Objective']}
        - Risk Tolerance: {user_profile['Factor']}
        - Investment Duration: {user_profile['Duration']}
        - Return Expectation: {user_profile['Expect']}
        - Current Preferred Avenue: {user_profile['Avenue']}
        
        {context}
        
        Provide personalized investment advice considering:
        1. Suitable investment avenues based on risk tolerance and duration
        2. Asset allocation recommendations
        3. Potential risks to consider
        4. Monitoring strategy
        5. Alternative options to consider
        
        Structure your response with clear headings and bullet points.
        All data retrun as proper blog article and HTML formate.
        Totla 750 words report only.
        Contact for more details advice: 
        contact@financialadvisor.com
        www.financialadvisor.com
        +44 77123 45689
        """
        
        print("AI api call")
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a knowledgeable financial advisor providing personalized investment recommendations. Generate the blog post in clean HTML format using tags like <h1>, <h2>, <p>, <ul>, <li>, and <strong>. Do not include any Markdown or plain text. Only return valid HTML that can be directly used in a WordPress post."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def get_financial_advice(self, age, gender, objective, factor, duration, expect, avenue):
        user_profile = {
            'age': age,
            'gender': gender,
            'Objective': objective,
            'Factor': factor,
            'Duration': duration,
            'Expect': expect,
            'Avenue': avenue
        }
        print("Create user profile")
        
        profile_text = f"""
        Gender: {gender}
        Age: {age}
        Investment Objective: {objective}
        Primary Investment Factor: {factor}
        Investment Duration: {duration}
        Return Expectation: {expect}
        Preferred Investment Avenue: {avenue}
        """
        print("Create profile text")
        
        query_embedding = self.embedding_model.encode(profile_text)
        print("Create query_embedding")
        similar_profiles = self._find_similar_profiles(query_embedding)
        advice = self._generate_advice(user_profile, similar_profiles)
        print(advice)



        if advice.startswith("```html"):
            advice = advice[7:]  # removes ```html\n
        if advice.endswith("```"):
            advice = advice[:-3]  # removes \n``` or ```

        # filename = Path(f"advice_data.html")
        # with open(filename, "w", encoding="utf-8") as file:
        #     file.write(advice)
        similar_profiles_percentage = round((len(similar_profiles) / self.total_profiles) * 100, 2)
        return {
            'advice': advice,
            'similar_profiles': similar_profiles,
            'similar_profiles_percentage': similar_profiles_percentage,
            'user_profile': user_profile
        }