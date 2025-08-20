import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

/**
 * Discord Webhook Handler for La Vida Luca App
 * Handles Discord events, slash commands, and bot interactions
 */

const DISCORD_WEBHOOK_SECRET = process.env.DISCORD_WEBHOOK_SECRET;
const DISCORD_BOT_TOKEN = process.env.DISCORD_BOT_TOKEN;
const DISCORD_GUILD_ID = process.env.DISCORD_GUILD_ID;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const signature = request.headers.get('x-signature-ed25519');
    const timestamp = request.headers.get('x-signature-timestamp');

    // Verify Discord signature (simplified - use actual verification in production)
    if (!verifyDiscordSignature(await request.text(), signature, timestamp)) {
      return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
    }

    logger.info('Discord webhook received', { 
      type: body.type, 
      id: body.id 
    });

    // Handle Discord interaction types
    switch (body.type) {
      case 1: // PING
        return NextResponse.json({ type: 1 }); // PONG

      case 2: // APPLICATION_COMMAND
        return await handleSlashCommand(body);

      case 3: // MESSAGE_COMPONENT
        return await handleMessageComponent(body);

      case 4: // APPLICATION_COMMAND_AUTOCOMPLETE
        return await handleAutocomplete(body);

      case 5: // MODAL_SUBMIT
        return await handleModalSubmit(body);

      default:
        logger.warn('Unknown Discord interaction type', { type: body.type });
        return NextResponse.json({ error: 'Unknown interaction type' }, { status: 400 });
    }

  } catch (error) {
    logger.error('Error processing Discord webhook', { error });
    return NextResponse.json(
      { error: 'Webhook processing failed' },
      { status: 500 }
    );
  }
}

/**
 * Handle slash commands
 */
async function handleSlashCommand(interaction: any) {
  const { data, member, user } = interaction;
  const commandName = data.name;

  logger.info('Discord slash command received', {
    command: commandName,
    user: user?.username || member?.user?.username,
    guildId: interaction.guild_id,
  });

  switch (commandName) {
    case 'activities':
      return await handleActivitiesCommand(interaction);

    case 'suggest':
      return await handleSuggestCommand(interaction);

    case 'profile':
      return await handleProfileCommand(interaction);

    case 'help':
      return await handleHelpCommand(interaction);

    case 'stats':
      return await handleStatsCommand(interaction);

    default:
      return createResponse({
        type: 4, // CHANNEL_MESSAGE_WITH_SOURCE
        data: {
          content: `Commande inconnue: ${commandName}`,
          flags: 64, // EPHEMERAL
        },
      });
  }
}

/**
 * Handle message components (buttons, select menus)
 */
async function handleMessageComponent(interaction: any) {
  const { data, member, user } = interaction;
  const customId = data.custom_id;

  logger.info('Discord message component interaction', {
    customId,
    componentType: data.component_type,
    user: user?.username || member?.user?.username,
  });

  switch (customId) {
    case 'view_activity':
      return await handleViewActivityButton(interaction);

    case 'join_activity':
      return await handleJoinActivityButton(interaction);

    case 'activity_category':
      return await handleActivityCategorySelect(interaction);

    default:
      return createResponse({
        type: 4,
        data: {
          content: 'Action non reconnue.',
          flags: 64,
        },
      });
  }
}

/**
 * Handle autocomplete for commands
 */
async function handleAutocomplete(interaction: any) {
  const { data } = interaction;
  const focusedOption = data.options?.find((option: any) => option.focused);

  if (!focusedOption) {
    return createResponse({
      type: 8, // APPLICATION_COMMAND_AUTOCOMPLETE_RESULT
      data: { choices: [] },
    });
  }

  const choices = await getAutocompleteChoices(focusedOption.name, focusedOption.value);

  return createResponse({
    type: 8,
    data: { choices },
  });
}

/**
 * Handle modal submissions
 */
async function handleModalSubmit(interaction: any) {
  const { data, member, user } = interaction;
  const customId = data.custom_id;

  logger.info('Discord modal submission', {
    customId,
    user: user?.username || member?.user?.username,
  });

  switch (customId) {
    case 'suggestion_modal':
      return await handleSuggestionModal(interaction);

    case 'feedback_modal':
      return await handleFeedbackModal(interaction);

    default:
      return createResponse({
        type: 4,
        data: {
          content: 'Formulaire non reconnu.',
          flags: 64,
        },
      });
  }
}

/**
 * Handle /activities command
 */
async function handleActivitiesCommand(interaction: any) {
  const category = interaction.data.options?.find((opt: any) => opt.name === 'category')?.value;
  
  // Fetch activities from your API
  const activities = await fetchActivities(category);

  const embeds = activities.slice(0, 3).map((activity: any) => ({
    title: activity.title,
    description: activity.summary,
    color: 0x00ff00,
    fields: [
      { name: 'Catégorie', value: activity.category, inline: true },
      { name: 'Durée', value: `${activity.duration_min} min`, inline: true },
      { name: 'Niveau', value: `${activity.safety_level}/5`, inline: true },
    ],
    footer: { text: `ID: ${activity.id}` },
  }));

  const components = [{
    type: 1, // ACTION_ROW
    components: [
      {
        type: 2, // BUTTON
        style: 1, // PRIMARY
        label: 'Voir plus d\'activités',
        custom_id: 'view_more_activities',
      },
      {
        type: 2, // BUTTON
        style: 2, // SECONDARY
        label: 'Filtrer par catégorie',
        custom_id: 'filter_activities',
      },
    ],
  }];

  return createResponse({
    type: 4,
    data: {
      content: `**Activités ${category ? `de la catégorie ${category}` : 'disponibles'}:**`,
      embeds,
      components,
    },
  });
}

/**
 * Handle /suggest command
 */
async function handleSuggestCommand(interaction: any) {
  const modal = {
    title: 'Suggérer une activité',
    custom_id: 'suggestion_modal',
    components: [
      {
        type: 1, // ACTION_ROW
        components: [{
          type: 4, // TEXT_INPUT
          custom_id: 'activity_title',
          label: 'Titre de l\'activité',
          style: 1, // SHORT
          required: true,
          max_length: 100,
        }],
      },
      {
        type: 1,
        components: [{
          type: 4,
          custom_id: 'activity_description',
          label: 'Description',
          style: 2, // PARAGRAPH
          required: true,
          max_length: 1000,
        }],
      },
      {
        type: 1,
        components: [{
          type: 4,
          custom_id: 'activity_category',
          label: 'Catégorie',
          style: 1,
          required: false,
          placeholder: 'agriculture, élevage, nature...',
        }],
      },
    ],
  };

  return createResponse({
    type: 9, // MODAL
    data: modal,
  });
}

/**
 * Handle /profile command
 */
async function handleProfileCommand(interaction: any) {
  const user = interaction.user || interaction.member?.user;
  
  // Fetch user profile from your API
  const userProfile = await fetchUserProfile(user.id);

  const embed = {
    title: `Profil de ${user.username}`,
    color: 0x0099ff,
    thumbnail: { url: `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png` },
    fields: [
      { name: 'Compétences', value: userProfile?.skills?.join(', ') || 'Aucune', inline: true },
      { name: 'Localisation', value: userProfile?.location || 'Non renseignée', inline: true },
      { name: 'Activités réalisées', value: userProfile?.activitiesCount?.toString() || '0', inline: true },
    ],
    timestamp: new Date().toISOString(),
  };

  return createResponse({
    type: 4,
    data: { embeds: [embed] },
  });
}

/**
 * Handle /help command
 */
async function handleHelpCommand(interaction: any) {
  const embed = {
    title: '🌱 Aide La Vida Luca Bot',
    description: 'Voici les commandes disponibles:',
    color: 0x00ff00,
    fields: [
      {
        name: '/activities [category]',
        value: 'Affiche les activités disponibles, optionnellement filtrées par catégorie',
      },
      {
        name: '/suggest',
        value: 'Ouvre un formulaire pour suggérer une nouvelle activité',
      },
      {
        name: '/profile',
        value: 'Affiche votre profil et vos statistiques',
      },
      {
        name: '/stats',
        value: 'Affiche les statistiques générales de la plateforme',
      },
    ],
    footer: {
      text: 'La Vida Luca - Plateforme collaborative pour la formation agricole',
    },
  };

  return createResponse({
    type: 4,
    data: { embeds: [embed] },
  });
}

/**
 * Handle /stats command
 */
async function handleStatsCommand(interaction: any) {
  // Fetch platform statistics
  const stats = await fetchPlatformStats();

  const embed = {
    title: '📊 Statistiques La Vida Luca',
    color: 0xff9900,
    fields: [
      { name: 'Activités totales', value: stats.totalActivities?.toString() || '0', inline: true },
      { name: 'Utilisateurs actifs', value: stats.activeUsers?.toString() || '0', inline: true },
      { name: 'Suggestions reçues', value: stats.suggestions?.toString() || '0', inline: true },
    ],
    timestamp: new Date().toISOString(),
  };

  return createResponse({
    type: 4,
    data: { embeds: [embed] },
  });
}

/**
 * Utility functions
 */
function verifyDiscordSignature(body: string, signature: string | null, timestamp: string | null): boolean {
  // Implement proper Discord signature verification
  // For now, just check if secret exists
  return !!DISCORD_WEBHOOK_SECRET;
}

function createResponse(response: any) {
  return NextResponse.json(response);
}

async function fetchActivities(category?: string) {
  // Mock data - replace with actual API call
  return [
    {
      id: '1',
      title: 'Soins aux poules',
      summary: 'Apprendre les bases de l\'élevage de volailles',
      category: 'elevage',
      duration_min: 60,
      safety_level: 2,
    },
    {
      id: '2',
      title: 'Plantation de légumes',
      summary: 'Techniques de plantation en agriculture biologique',
      category: 'agriculture',
      duration_min: 90,
      safety_level: 1,
    },
  ];
}

async function fetchUserProfile(discordUserId: string) {
  // Mock data - replace with actual API call
  return {
    skills: ['elevage', 'agriculture'],
    location: 'Bretagne',
    activitiesCount: 5,
  };
}

async function fetchPlatformStats() {
  // Mock data - replace with actual API call
  return {
    totalActivities: 42,
    activeUsers: 156,
    suggestions: 23,
  };
}

async function getAutocompleteChoices(optionName: string, value: string) {
  if (optionName === 'category') {
    const categories = ['agriculture', 'elevage', 'nature', 'hygiene'];
    return categories
      .filter(cat => cat.includes(value.toLowerCase()))
      .slice(0, 25)
      .map(cat => ({ name: cat, value: cat }));
  }
  return [];
}

async function handleSuggestionModal(interaction: any) {
  const components = interaction.data.components;
  const title = components[0]?.components[0]?.value;
  const description = components[1]?.components[0]?.value;
  const category = components[2]?.components[0]?.value;

  // Save suggestion to your database
  logger.info('New activity suggestion', { title, description, category });

  return createResponse({
    type: 4,
    data: {
      content: '✅ Merci pour votre suggestion ! Elle sera examinée par notre équipe.',
      flags: 64,
    },
  });
}

async function handleFeedbackModal(interaction: any) {
  // Handle feedback modal submission
  return createResponse({
    type: 4,
    data: {
      content: '✅ Merci pour votre retour !',
      flags: 64,
    },
  });
}

async function handleViewActivityButton(interaction: any) {
  // Handle view activity button
  return createResponse({
    type: 4,
    data: {
      content: 'Fonctionnalité en cours de développement...',
      flags: 64,
    },
  });
}

async function handleJoinActivityButton(interaction: any) {
  // Handle join activity button
  return createResponse({
    type: 4,
    data: {
      content: 'Inscription à l\'activité réussie !',
      flags: 64,
    },
  });
}

async function handleActivityCategorySelect(interaction: any) {
  // Handle activity category selection
  return createResponse({
    type: 4,
    data: {
      content: 'Filtrage par catégorie appliqué.',
      flags: 64,
    },
  });
}