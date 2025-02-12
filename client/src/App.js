import { Input, List, Button, Avatar, Flex, Divider } from 'antd';
import './App.css';
import { useState } from 'react';
import { motion } from 'framer-motion';

function App() {
  const botAvatar = 'https://img.freepik.com/premium-vector/3d-chat-bot-robot_685294-11.jpg?semt=ais_hybrid'
  const userAvatar = 'https://static-00.iconduck.com/assets.00/user-avatar-happy-icon-1023x1024-bve9uom6.png'
  
  const [ messages, setMessages ] = useState(
    [{'sender':'Bot',
      'content':'Hello this is Bot! What can I help you with?'
    },
    { 'sender':'User',
      'content':'I have a problem with Git merges'
    }]);

  const [ inputBox, setInputBox ] = useState('')

  const handleInputBox = (e) => {
    setInputBox(e.target.value);
  }

  const handleSendMessage = async (event) => {
    event.preventDefault();
    if(!inputBox.trim()) return;
    const newMsg = {'sender':'User',
              'content': inputBox}
    setMessages((prevMessages)=>([...prevMessages, newMsg]));
    setInputBox('');

    const response = await fetch('http://localhost:5000/chat',
      {
        'method': 'POST',
        'headers': {'Content-type' :'application/json'},
        'body': JSON.stringify(newMsg)

      }
    );
    const data = await response.json()
    setMessages((prevMessages) => ([...prevMessages, {'sender':'Bot', 'content': data.content}]))
  }

  return (
    <div className="App">
      <header className="App-header">
      <Flex vertical style={{ height: "100vh", maxWidth: "900px", margin: "0 auto" }}>
      <Flex  flex={1}  justify='center' style={{ overflowY: "auto", width: "100%",align:'center', padding: "10px" }}>
        <List 
          itemLayout='horizontal'
          dataSource={messages}
          renderItem={
            (msg) => (
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 4, y: 0 }}
                transition={{ duration: 0.3 }}>
                <Divider style={{borderColor: '#7cb305'}}>
                  {msg.sender==='Bot'? <Avatar src={botAvatar}/>:<Avatar src={userAvatar}/>}
                </Divider>
                  <p style={{fontSize:20, textAlign: "left"}}>{msg.content}</p>
              </motion.div>
            )
          }>

          </List>
        
        </Flex>
        <Flex justify="center" style={{borderTop: "1px solid #ddd"}}>
        <div>
        <Input.TextArea rows={4}
          size='large '
          placeholder='Type in a question or an issue!'
          value={inputBox}
          onChange={handleInputBox}
          onPressEnter={handleSendMessage}
          style={{ width: "70%", minWidth: "500px", marginBottom:'20px' }}/>
      </div>
          </Flex>
      </Flex>
      </header>
    </div>
  );
}

export default App;
