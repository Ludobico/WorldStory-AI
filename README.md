# WorldStory_AI

[![ko](https://img.shields.io/badge/lang-ko-green.svg)](./README.ko.md)

![Alt text](./frontend/src/components/Static/intro.gif)

## Introduction

WroldStory_AI is a project that creates and interacts with fictional characters

## Installation

To use WorldStory_AI, need to install the following programs

- python 3.10 or newer

- [Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable)

After installing the above programs, run the `InstallKit.bat` file to install both the frontend and backend libraries

if the batch file is not executed, or if you prefer to install it using commands, clone the WorldStory_AI repository and enter the following commands in sequence

- frontend

```bash
cd ./frontend
```

```bash
yarn install
```

- backend

```bash
cd backend
```

```bash
python -m venv worldstory_backend
```

```bash
cd worldstory_backend/Scripts/
```

```bash
activate
```

```bash
cd ../../
```

```bash
pip install -r requirements.txt
```

## Installation-LlamaCPP

To use [Llama-cpp](https://github.com/abetlen/llama-cpp-python), install the following additional libraries and programs

- [Cmake](https://cmake.org/download/)
- Visual Studio C++ 14.0 or newer

```bash
pip install llama-cpp-python
```

## Getting Started

After installing both the frontend and backend, execute the `StartKit.bat` file to launch the project.

if the batch file does not run, or if you prefer to run it using commands, enter the following commands in two seperate terminals withi the direcory where you downloaded the WorldStory_AI repository

- frondend

```bash
cd ./frontend
```

```bash
yarn start
```

- backend

```bash
./backend
```

```bash
cd ./worldstory_backend/Scripts
```

```bash
activate
```

```bash
cd ../../
```

```bash
uvicorn main:app --reload
```

## Create Character

![Alt text](./frontend/src/components/Static/create_character.gif)

You can create a character bt clicking the Character Setting button on the first screen. Choose either the GPT-3.5 model or the local Llama model([GGML](https://github.com/ggerganov/ggml)) to create your character

- Supported Llama Models
  - openbuddy-llama2-13b-v11.1.ggmlv3
  - puddlejumper-13b.ggmlv3
  - WizardLM-13B-1.0
  - kimiko-7b.ggmlv3
  - Kimiko-v2-13B-GGML

Download the Llama model from HuggingFace as a binary(.bin) file and place it in the [backend/Models](./backend/Models) folder to enable recognition

⚠️ The local Llama model is currently in the testing phase, the prompts and image generation features are all based on GPT-3.5

Under `Model Select`, choose GPT-3.5 and then click the `Generate` button to create the character

To interact with the created character, click the `Save Setting` button to store it in the [backend/Characters](./backend/Characters) folder

## User config

Before creating and interacting with a character, you can set the User's name, picture, and preferences for era, name, and gender. Create a user profile bt modifying the `UserConfig.ini` file in the [backend/Characters/User](./backend/Characters/User/) folder

![Alt text](./frontend/src/components/Static/user_config.png)

You can use the `language` option to converse in any language you prefer, but it is **set** to English when creating the character. The image generation feature based on the character's appearance only functions in English

The `memory` option determines the number of conversations the character can remember during a conversation. The higher the memory, the more previous conversations can be retained, but it should be set to a reasonable value, as some information may be lost if the token length is exceeded

The `era` option allows you to set the era you want your character to be from (e.g fantasy, cyberpunk, dystopia) when creating the character. If the value is empty, it will be generated randomly

The `gender` and `name` options also allow you to specify a gender and name when creating the character. If the values are empty, they will be generated randomly

![Alt text](./frontend/src/components/Static/user_profile.png)

If you want to change your profile image, simply delete the existing image in the [/backend/Characters/User](./backend/Characters/User/) path and replace it with the image you want

## Chat with Character

![Alt text](./frontend/src/components/Static/chatting.gif)

You can engage in a conversation with the character you created by clicking the `Chat with Character` button

![Alt text](./frontend/src/components/Static/chat_setting.png)

### GPT3.5 or LocalModel

You can choose either `GPT3.5` or `LlamaModel` as the model the conversation. The default setting is GPT3.5

⚠️ `LocalModel` is still in development and currently only functions with GPT3.5

### Character

When you create a character in the `Character setting`, go to the `Character` section to engage in a conversation with the character of your choice

### LLM Setting

Parameter values that can be configured in the LocalModel

⚠️ `LLM Setting` is still in development and currently only functions with GPT3.5

### Background

You can change the background to match the era of your character. You can choose from fantasy, cyberpunk, wild west and apocalyptic settings
