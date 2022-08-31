from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
from pade.acl.messages import ACLMessage  
import sys

class SenderAgent(Agent):
    def __init__(self, aid, receiver_agent, start=False):
        super().__init__(aid)
        self.receiver_agent = receiver_agent
        self.start = start
        

    def react(self, message):
        super().react(message)
        display_message(self.aid.localname, message.content)
        self.send_message(message.content)

    def on_start(self):
        super().on_start()
        if (self.start):
            self.send_message("")

    def send_message(self,msg):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(self.receiver_agent)
        self.add_all_agents(message.receivers)
        try:
            if msg == "Bye"or msg=="bye":
                sys.exit()
            else:    
               msg=input("Enter message to send: ")
        
            message.set_content(msg)
            self.send(message)
        except:
            print("Conversation ended....!!")
            
    def add_all_agents(self, receivers):
        for receiver in receivers:
            self.agentInstance.table[receiver.localname] = receiver


class ReceiverAgent(Agent):
    def __init__(self, aid):
        super().__init__(aid)

    def react(self, message):
        super().react(message)
        display_message(self.aid.localname, message.content)
        self.send_message(AID(message.sender.name), message.content)

    def send_message(self, receiver_agent, msg):
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
        message.add_receiver(receiver_agent)
        self.add_all_agents(message.receivers)
        try:
            if msg == "Bye" or msg=="bye":
                sys.exit()
            else:    
               msg=input("Enter message to send: ")
        
            message.set_content(msg)
            self.send(message)
        except:
            print("Conversation ended....!!")



    def add_all_agents(self, receivers):
        for receiver in receivers:
            self.agentInstance.table[receiver.localname] = receiver

if __name__ == '__main__':
    agents = list()
    
    # other system
    other_receiver_agent_aid = AID(name='receiver@192.168.1.11:{}'.format(30001))
    
    # current system
    sender_agent_aid = AID(name='sender@192.168.1.9:{}'.format(30000))
    sender_agent = SenderAgent(sender_agent_aid, other_receiver_agent_aid)
    agents.append(sender_agent)

    receiver_agent_aid = AID(name='receiver@192.168.1.9:{}'.format(30001))
    receiverAgent = ReceiverAgent(receiver_agent_aid)
    agents.append(receiverAgent)
    start_loop(agents)
