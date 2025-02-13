const { Client, IntentsBitField } = require('discord.js');
const { GoogleGenerativeAI } = require("@google/generative-ai");

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

client.on('ready', () => {
  console.log(`✅ Bot is online and ready`);
});

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
});

client.login(process.env.TOKEN);