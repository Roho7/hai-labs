"use client";
import axios from "axios";
import { useEffect, useState } from "react";
import { Response } from "./Response";
import { Send } from "react-feather";

interface ResponseType {
  data: string;
}

export const ChatBox = () => {
  const [chat, setChat] = useState<string>();
  const [placeholder, setPlaceholder] = useState("");
  const [response, setResponse] = useState<ResponseType>({ data: "" });
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setChat(e.target.value);
  };
  const getData = async (e: React.FormEvent) => {
    e.preventDefault();
    const msg = { msg: chat };
    try {
      const data = await axios.post("http://127.0.0.1:5000/chat", msg);
      setChat("");
      setResponse(data);
    } catch (err) {
      console.log(err);
    }
  };

  const placeholdersArr = [
    "Say 'Add cooking at 7pm' ",
    "Ask 'What can you do?'",
    "Ask 'What's up?'",
    "Ask 'What is the weather?'",
    "Ask about your day",
  ];
  useEffect(() => {
    setTimeout(() => {
      const rand = Math.floor(Math.random() * (3 - 1));
      setPlaceholder(placeholdersArr[rand]);
    }, 5000);
  }, [placeholder]);
  return (
    <div className="flex flex-col gap-2 w-full">
      <div>
        <Response msg={response.data} />
      </div>

      <form action="" onSubmit={getData} className="flex gap-2">
        <input
          type="text"
          className="text-black p-4 rounded-md bg-slate-200 w-full"
          onChange={handleChange}
          value={chat}
          placeholder={placeholder}
        />
        <button type="submit" className=" bg-yellow-600 p-4 rounded-md">
          <Send />
        </button>
      </form>
    </div>
  );
};
