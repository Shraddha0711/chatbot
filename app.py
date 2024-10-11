import chainlit as cl
import os
from model import create_chat_function
import mysql.connector
import plotly.graph_objects as go
import re
import pandas as pd
    
def query_database(query):

    conn = mysql.connector.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('database'))

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [description[0] for description in cur.description] if cur.description else []
    conn.close()
    return rows, columns

claude_chat=create_chat_function()

async def action_answer(action):
    res = claude_chat(action)
    query = (((res.split("```"))[1]).removeprefix("sql\n")).removesuffix("\n")
    rows,columns=query_database(query)
    df=pd.DataFrame(rows,columns=columns)  
    answer = res.split("```")[-1].removeprefix("\n\nSummary:\n") 
    
    if len(rows) == 0 :
        await cl.Message(content=f"{answer}\n\n**Count : {len(rows)}**").send()   
    elif len(rows)==1 and len(columns)==1:    
        await cl.Message(content=f"{answer}\n\n\n **The answer is : {rows[0][0]}**").send()  
    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        line_color='black',
                        align="left"),
            cells=dict(values=[df[i] for i in df.columns],
                        fill_color='white',line_color='black',
                        align="left"))],layout=dict(autosize=True))
        fig.update_layout(autosize=False,
                            width=800,
                            height=400,
                            margin=dict(l=10,r=10,t=10,b=10),
                            paper_bgcolor = "rgba(0, 0, 0, 0)")
        await cl.Message(content=f"{answer}\n\n**Count : {len(rows)}**", elements=[cl.Plotly(name="chart", figure=fig, display="inline")]).send()
        df.to_csv("output.csv",sep = ",",index=False)
        elements = [cl.File(name="data.csv",path="output.csv",display="inline",mime="text/csv")]
        await cl.Message(content="**Download the data as CSV file**", elements=elements).send()



@cl.action_callback("Customers with no activity after unlock?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Customers active after app download?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Offers with highest redemption?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Offers with lowest redemption?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Users who never redeemed offers?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Total offers redeemed?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.action_callback("Total points issued?")
async def on_action(action: cl.Action):
    act = action.name
    await action_answer(act)

@cl.on_chat_start
async def on_chat_start():
    text = """
        Hello there! 👋
        I'm Smartola, your AI-powered chatbot, here to guide you through the world of Rewardola.
        Let's get start.
        """
    actions=[
            cl.Action(name = "Customers with no activity after unlock?",value='option_1'),
            cl.Action(name = "Customers active after app download?",value='option_2'),
            cl.Action(name = "Offers with highest redemption?",value='option_3'),
            cl.Action(name = "Offers with lowest redemption?",value='option_4'),
            cl.Action(name = "Users who never redeemed offers?",value='option_5'),
            cl.Action(name = "Total offers redeemed?",value='option_6'),
            cl.Action(name = "Total points issued?",value='option_7'),
        ]
    await cl.Message(content=text,actions=actions).send()
    # await cl.Message(content=text).send()

@cl.on_message
async def main(message: cl.Message):

    res=claude_chat(message.content)
    # print(res)
    if "```sql" in res:
        query = (((res.split("```"))[1]).removeprefix("sql\n")).removesuffix("\n")
        key_words = r"\b(DELETE|UPDATE|INSERT|CREATE|TRUNCATE|SET)\b"
        if re.search(key_words, query, flags=re.IGNORECASE):      
            msg = "I am sorry, I am unable to modify the existing database. I am an AI chatbot designed to analyze data from the Rewardola platform and can only provide insights based on user quesions.If you need to modify data, you can use the appropriate database management tools or consult with a database administrator."  
            await cl.Message(content=msg).send()
        else:
            rows,columns=query_database(query)
            df=pd.DataFrame(rows,columns=columns)  
            answer = res.split("```")[-1].removeprefix("\n\nSummary:\n") 
            
            if len(rows) == 0 :
                await cl.Message(content=f"{answer}\n\n**Count : {len(rows)}**").send()   
            elif len(rows)==1 and len(columns)==1:    
                await cl.Message(content=f"{answer}\n\n\n **The answer is : {rows[0][0]}**").send()  
            else:
                fig = go.Figure(data=[go.Table(
                    header=dict(values=list(df.columns),
                                line_color='black',
                                align="left"),
                    cells=dict(values=[df[i] for i in df.columns],
                               fill_color='white',line_color='black',
                               align="left"))],layout=dict(autosize=True))
                fig.update_layout(autosize=False,
                                  width=800,
                                     height=400,
                                  margin=dict(l=10,r=10,t=10,b=10),
                                  paper_bgcolor = "rgba(0, 0, 0, 0)")
                await cl.Message(content=f"{answer}\n\n**Count : {len(rows)}**", elements=[cl.Plotly(name="chart", figure=fig, display="inline")]).send()
                df.to_csv("output.csv",sep = ",",index=False)
                elements = [cl.File(name="data.csv",path="output.csv",display="inline",mime="text/csv")]
                await cl.Message(content="**Download the data as CSV file**", elements=elements).send()
    else:
        await cl.Message(content=res).send()
