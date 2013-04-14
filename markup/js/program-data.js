var programData = {};

programData.flows = [
    {id: 1, title: 'Зал 1', startTime: '10:00'},
    {id: 2, title: 'Зал 2', startTime: '16:00'},
    {id: 3, title: 'Холл', startTime: '9:00'}
];

programData.items = [
    {
        title: 'Точка зрения или как начать делать швабру', person: 'Ольга Курилова',
        flowId: 1, duration: 15
    }, {
        title: 'Доклад про дружбу', person: 'Сергей Петров',
        flowId: 1, duration: 30
    }, {
        title: 'Похождения одного матроса', person: 'Дмитрий Михеев',
        flowId: 1, duration: 10
    }, {
        title: 'Школа швабр: как получить швабру из студента за полгода', person: 'Алексей Митричев',
        flowId: 1, duration: 15
    }, {
        title: 'Пример двух одновременных событий', person: 'Геннадий Малахов',
        flowId: 1, duration: 20, slot: 1
    }, {
        title: 'Пример двух одновременных событий', person: 'Николае Чаушеску',
        flowId: 1, duration: 20, slot: 2
    },

    {
        title: 'Похождения одного благонамеренного', person: 'Иван Станюкевич',
        flowId: 2, duration: 20, startTime: '10:30'
    }, {
        title: 'Кристалл воображения', person: 'Владимир Казанцев',
        flowId: 2, duration: 15
    }, {
        title: 'Искусство наступать на швабру', person: 'Алекс Кротов',
        flowId: 2, duration: 10
    }, {
        title: 'Взаимодействие пользователя и швабры. Методики описания и визуализации', person: 'Олег Артамонов',
        flowId: 2, duration: 20
    },

    {
        title: 'Секретная техника фабрики швабр', person: 'Сергей Шемякин',
        flowId: 3, duration: 15, startTime: '9:00'
    }, {
        title: 'Словарь морских терминов, встречающихся в рассказах', person: 'Андрей Паничев',
        flowId: 3, duration: 20
    }, {
        title: 'Курс молодой швабры', person: 'Юрий Лебедев',
        flowId: 3, duration: 10
    }, {
        title: '10 способов мыть быстрее', person: 'Искандер Иванов',
        flowId: 3, duration: 30
    }, {
        title: 'Формирование команды', person: 'Ирина Алексеева',
        flowId: 3, duration: 15
    },

    {
        title: 'Кофе брейк',
        duration: 60
    }
];