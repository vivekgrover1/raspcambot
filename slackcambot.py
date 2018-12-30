import os
import time
import subprocess
from slackclient import SlackClient
import slack_cmd_process
import threading

def get_bot_id(BOT_NAME,slack_client):
    """
        This function gets the id of bot based on its name in slack team.
        We need the id because it allows us to parse the message directed at bot.

    """
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
       users = api_call.get('members')
       for user in users:
           if 'name' in user and user.get('name') == BOT_NAME:
             return (user.get('id'))



def handle_command(command, channel,msg_id,user_id):
    """
        Receives commands directed at the bot and sends to function cmd_process
        to process the command , which returns the response. Based on response it post the
        message to slack thread or message.
    """

    response,color=slack_cmd_process.cmd_process(command)

#    if msg_id == "Thread_False":
#        slack_client.api_call("chat.postMessage", channel=channel,
#                text="<@%s> " %user_id , as_user=True,attachments=[{"text": "%s" %response,"color":"%s" %color}])
#    else:
#        slack_client.api_call("chat.postMessage", channel=channel,
#                text="<@%s> " %user_id, as_user=True,thread_ts=msg_id,attachments=[{"text": "%s" %response,"color":"%s" %color}])


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function parse the message directed at bot based on its id
        and return None otherwise.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text'] and 'thread_ts' in output:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel'], output['thread_ts'],output['user']
            elif output and 'text' in output and AT_BOT in output['text']:
                   return output['text'].split(AT_BOT)[1].strip().lower(), \
                         output['channel'],"Thread_False",output['user']

    return None, None, None, None

def process_slack_output(cmd,chn,msg,usr):
    """
        Message directed at bot is created into thread , to speed up the
        processing of the message.
    """

    t = threading.Thread(target=handle_command, args=(cmd,chn,msg,usr,))
    threads.append(t)
    t.start()


if __name__ == "__main__":

      slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
      BOT_NAME= os.environ.get('CHATBOT_NAME')
      BOT_ID = get_bot_id(BOT_NAME,slack_client)
      AT_BOT = "<@" + BOT_ID + ">"
      threads = []

      WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
      if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
           sc=slack_client.rtm_read()
           print (sc)
           command, channel, msg_id,user_id = parse_slack_output(sc)
           print (command, channel, msg_id, user_id)
           
           if command and channel and msg_id and user_id:
              process_slack_output(command,channel,msg_id,user_id)
           time.sleep(WEBSOCKET_DELAY)
      else:
         print("Connection failed. Invalid Slack token or bot ID?")

