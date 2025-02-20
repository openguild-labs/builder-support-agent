const { Client, IntentsBitField } = require('discord.js');
const { GoogleGenerativeAI } = require("@google/generative-ai");
const { Chroma } = require('chromadb');
const { RecursiveCharacterTextSplitter } = require('langchain/text_splitter');
const { RetrievalQAWithSourcesChain } = require('langchain/chains')
const { Document } = require('langchain/document');
const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" })

const client = new Client({
  intents: [
    IntentsBitField.Flags.Guilds,
    IntentsBitField.Flags.GuildMembers,
    IntentsBitField.Flags.GuildMessages,
    IntentsBitField.Flags.MessageContent,
  ],
});

const repoPath = "../docs/";

function readMarkdownFiles(directory) {
  if (!fs.existsSync(directory)) {
    console.log(`❌ Thư mục không tồn tại: ${directory}`);
    return [];
  }

  const allDocuments = [];
  const files = fs.readdirSync(directory);

  files.forEach((file) => {
    if (file.endsWith('.md')) {
      const filePath = path.join(directory, file);
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const doc = new Document({ page_content: content, metadata: { source: filePath } });
        allDocuments.push(doc);
      } catch (error) {
        console.error(`❌ Không đọc được file ${filePath}: ${error}`);
      }
    }
  });

  return allDocuments
}
// Function to get latest commits from GitHub
async function getLatestCommits() {
  const { Octokit } = await import("@octokit/rest");
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  const { data: commits } = await octokit.repos.listCommits({
    owner: 'w3f',
    repo: 'polkadot-wiki',
    per_page: 5,
  });

  const commitMessages = [];

  for (const commit of commits) {
    const { data: commitDetails } = await octokit.repos.getCommit({
      owner: 'w3f',
      repo: 'polkadot-wiki',
      ref: commit.sha,
  });
  const files = commitDetails.files ? commitDetails.files.filter(file => file.filename.startsWith('docs/')) : [];

  if (files.length > 0) {
      commitMessages.push(
          `**Date:** ${commit.commit.author.date}\n**URL:** ${commit.html_url}\n**Changed files:**\n${files.map(file => `- ${file.filename} (modified)`).join('\n')}`
      );
  }
  }

  return commitMessages.join('\n\n');
}
// Function to get latest blog posts
async function getLatestBlogPosts() {

  console.log('🔍 Fetching the blog page...');
  try {
    const response = await axios.get('https://polkadot.network/blog');
    const $ = cheerio.load(response.data);

    const posts = [];
    $('.col-span-full').each((i, element) => {
      const title = $(element).find('h2').text().trim();
      const link = $(element).find('h2 a').attr('href');
      if (title && link) {
        posts.push(`**New Blog Post:** ${title}\n**Link:** https://polkadot.network${link}`);
      }
    });

    return posts.slice(0, 1).join('\n\n');
  } catch (error) {
    console.error(`⚠️ Error fetching the blog page: ${error}`);
    return '⚠️ Error fetching the blog page.';
  }
}


// Function ready discord
client.on('ready', () => {
  console.log(`✅ Bot is online and ready`);
});
// Interaction create
client.on('interactionCreate', async (interaction) => {
  if (!interaction.isCommand()) return;

  const { commandName } = interaction;

  if (commandName === 'ask') {
    await interaction.deferReply();

    const userQuestion = interaction.options.getString('question');

    try {

      const TIME_LIMIT = 10 * 1000;

      const aiResponse = Promise.race([
        model.generateContent({
          contents: [
            { 
              role: 'user', 
              parts: [{ text: userQuestion }] 
            }
          ],
          generationConfig: 
          { 
            maxOutputTokens: 1000, 
            temperature: 0.7 
          }
        }),
        new Promise((_, reject) => setTimeout(() => reject(new Error("TIMEOUT")), TIME_LIMIT))
      ]);

      const result = await aiResponse;
      const responseText = result.response.text();

      // Send the response to the Discord bot 
      await interaction.editReply({
        content: `**Question:** ${userQuestion}\n**Answer:**${responseText}`,
      });

      console.log(`User asked: ${userQuestion}`);
      console.log(`Gemini AI responded: ${responseText}`);
    } catch (error) {
      console.error(error);
      let errorMessage = "❌ An error occurred while processing your request.";
      if (error.message === "TIMEOUT") {
        errorMessage = "⏳ AI is taking too long to respond. Please try again later.";
      }

      await interaction.editReply({ content: errorMessage });
    }
  }

  if (commandName === 'noti') {
    await interaction.deferReply();

    const subCommand = interaction.options.getSubcommand();

    try {
      if (subCommand === 'commit') {
        const commits = await getLatestCommits();
        await interaction.editReply({ content: commits });
      } else if (subCommand === 'blog') {
        const blogPosts = await getLatestBlogPosts();
        await interaction.editReply({ content: blogPosts });
      }
    } catch (error) {
      console.error(error);
      if (interaction.deferred) {
        await interaction.editReply({ content: '❌ An error occurred while fetching notifications.' });
      } else {
        await interaction.reply({ content: '❌ An error occurred while fetching notifications.', ephemeral: true });
      }
    }
  }
});

client.login(process.env.TOKEN);