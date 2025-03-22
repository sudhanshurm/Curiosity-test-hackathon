📊 Curiosity: AI Assistant for Cost
Curiosity is an intelligent assistant that combines multiple data sources of Cost to provide insights into the working of departments and help identify opportunities. Using natural language processing, it allows users to query complex cost data without needing SQL knowledge.

🌟 Features
Natural Language Queries: Ask questions about your cost data in plain English
Automatic SQL Generation: Translates natural language to SQL queries
Interactive Visualizations: Automatically suggests and creates appropriate visualizations
Conversation Context: Maintains conversation history for follow-up questions
Error Handling: Gracefully handles query errors and provides feedback

🚀 Getting Started
Prerequisites
Python 3.8+
AWS account with access to Bedrock
Cost data in CSV format
Installation
Clone the repository:
git clone https://github.com/sudhanshurm/Curiosity-test-hackathon.git
cd Curiosity-test-hackathon
Create a Python virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt

Set up your AWS credentials:
# Example configuration - replace with your specific details
export AWS_CONFIG_FILE=~/.aws/credentials
export AWS_DEFAULT_PROFILE=mfa

Database Setup
Place your cost data CSV file in the project directory
Run the database setup script:
python setup_database.py
This will create the SQLite database (publish_layer_1.db) with your cost data.

🔧 Configuration
The application uses AWS Bedrock for AI capabilities. You'll need to configure your AWS credentials:

# Example configuration in the application
os.environ['AWS_CONFIG_FILE'] = '/path/to/your/.aws/credentials'
os.environ['AWS_DEFAULT_PROFILE'] = 'your-profile'
If you're behind a corporate proxy:

os.environ['REQUESTS_CA_BUNDLE'] = '/path/to/your/cacert.pem'
os.environ['HTTPS_PROXY'] = "http://your-proxy-address:port"
🖥️ Usage
Start the Streamlit application:
streamlit run app.py
Open your browser and navigate to the provided URL (typically http://localhost:8501 )

Ask questions about your cost data in natural language, for example:

"What are the total costs by department?"
"Show me the trend of expenses over the last 6 months"
"Which projects exceeded their budget in Q2?"
"Compare labor costs across departments"
The application will:

Generate and execute the appropriate SQL query
Display the results in a table
Create a visualization if appropriate
Provide a natural language explanation of the findings

🔒 Security Considerations
The application requires AWS credentials with access to Bedrock
Database queries are generated from user input, but SQL injection is mitigated through parameterization
Consider your data privacy requirements when deploying this application
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.