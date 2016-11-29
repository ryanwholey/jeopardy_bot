var token = process.env.SLACK_TOKEN;

if (!token) {
    throw new Error('No slack token set, export SLACK_TOKEN=$TOKEN from the command line');
}
var Bot = require('slackbots');
var actions = require('./actions');
var utils = require('./utils');

var bot = new Bot({
    token: token,
    name: 'Trabek Bot'
});

bot.config = {
    icon_emoji: ':man:',
    greeting: '...and now here\'s the host of Jeopardy!, Trabek Bot!',
    questionTime: 80, // time in seconds
    timesUpMessages: [
        'Oop time\'s up, the correct answer is ',
        'Aaand the answer we were looking for is ',
        'NOPE! The correct answer is ',
        'I\'m sorry, the answer we were looking for is '
    ]
};

bot.state = {
    question: null
};

var validCommands = {
    'question': _handleRandomQuestion,
    'scores': _handleScores,
    'buzz': _handleAnswer,
    'answer': _handleAnswer,
    'help': _handleMenu,
    'menu': _handleMenu
};

var commandDescriptions = {
    'question': 'Ask Trebek for a question',
    'scores': 'List the scores of all players',
    'buzz': 'Answer one of Trebek\'s questions',
    'help': 'List the commands and rules',
};

var actionMap = {
    'ANSWER_WITH_TYPE': actions.fireAnswerWithType.bind(bot),
    'MENU': actions.fireMenu.bind(bot),
    'ANSWER_NO_QUESTION': actions.fireAnswerNoQuestion.bind(bot),
    'ANSWER': actions.fireAnswer.bind(bot),
    'UNSET_QUESTION': actions.fireUnsetQuestion.bind(bot),
    'MID_QUESTION': actions.fireMidQuestion.bind(bot),
    'SET_QUESTION': actions.fireGetQuestion.bind(bot),
    'SCORES': actions.fireGetScores.bind(bot)
};

/**
 * handler for !trabek question
 * if there's currently a question fire mid question response
 * else fire question action with UNSET_QUESTION callback
 */
function _handleRandomQuestion(options, params) {
    if (bot.state.question) {
        actionMap['MID_QUESTION'](options, params);
    } else {
        actionMap['SET_QUESTION'](options, params, actionMap['UNSET_QUESTION']);
    }
}

function _handleScores(options, params) {
    actionMap['SCORES'](options, params);
}

function _handleAnswer(options, params) {
    if (bot.state.question) {
        options.handleAnswerWithType = actionMap['ANSWER_WITH_TYPE'];
        options.handleUnsetQuestion = actionMap['UNSET_QUESTION'];
        actionMap['ANSWER'](options, params);
    } else {
        actionMap['ANSWER_NO_QUESTION'](options, params);
    }
}

function _handleMenu(options, params) {
    options.menu = commandDescriptions;

    actionMap['MENU'](options, params);
}

function _addHashAttributeToBot(data, attribute) {
    this[attribute + 'ById'] = data[attribute].reduce(function(memo, attr) {
        memo[attr.id] = attr.name;
        return memo;
    }, {});
}

function _computeChannelsById(data) {
    _addHashAttributeToBot.call(this, data, 'channels');
}

function _computeUsersById(data) {
    _addHashAttributeToBot.call(this, data, 'members');
}

bot.on('start', function() {
    this.getChannels()
        .then(_computeChannelsById.bind(this))
        .fail(utils.handleError.bind(this, 'Error hashing channels'));

    this.getUsers()
        .then(_computeUsersById.bind(this))
        .fail(utils.handleError.bind(this, 'Error hashing users'));

    // loading timeout lets table bot ignore already thrown tables
    bot.isLoading = true;

    setTimeout(function() {
        console.log(bot.config.greeting);
        bot.isLoading = false;
    }, 2000);
});

bot.on('message', function(msg) {
    if (msg && msg.text && !bot.isLoading) {

        var msgArray = msg.text.split(' ');

        if (msgArray[0] === '!trabek' || msgArray[0] === '!buzz') {
            var channelName = bot.channelsById[msg.channel];
            var userName = bot.membersById[msg.user];

            var options = {
                userName: userName,
                channelName: channelName,
                msgArray: msgArray
            };

            var params = {
                icon_emoji: bot.config.icon_emoji
            };

            if (msgArray[0] === '!buzz') {
                validCommands['buzz'](options, params);
            } else if (validCommands[msgArray[1]]) {
                validCommands[msgArray[1]](options, params);
            }
        }
    }
});
