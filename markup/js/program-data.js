/**
 * Saved from http://2013.profsoux.ru/api/schedule/
 */
var programData = {};

programData.flows = [

    {
        id: 1,
        title: 'Холл',
        code: 'flow_1',
        startTime: '10:00',
    },

    {
        id: 2,
        title: 'Большой зал',
        code: 'flow_2',
        startTime: '10:00',
    },

    {
        id: 3,
        title: 'Малый зал',
        code: 'flow_3',
        startTime: '14:30',
    },

    {
        id: 4,
        title: 'Зал на II этаже',
        code: 'flow_4',
        startTime: '14:30',
    }

];

programData.items = [

    {
        title: 'Регистрация, приветственный кофе',

        startTime: '10:00',

        flowId: [1],
        duration: 25,

        category: ''
    },

    {
        title: 'Как начать? Боремся со страхом чистого листа в проектиров...',

        href: '/papers/45/',

        startTime: '10:25',

        person: 'Ольга Павлова',

        flowId: [1],
        duration: 20,

        slot: 1,

        category: 'analytics'
    },

    {
        title: 'Православные Командиры. UX-принципы для профессионалов',

        href: '/papers/39/',

        startTime: '10:45',

        person: 'Стас Фомин',

        flowId: [1],
        duration: 15,

        slot: 2,

        category: 'analytics'
    },

    {
        title: 'Кручу-верчу, запутать хочу',

        href: '/papers/43/',

        startTime: '11:00',

        person: 'Никита Ефимов',

        flowId: [1],
        duration: 15,

        category: 'analytics'
    },

    {
        title: 'Sketchnotes',

        href: '/papers/37/',

        startTime: '11:15',

        person: 'Николай Чуприянов',

        flowId: [1],
        duration: 15,

        category: 'analytics'
    },

    {
        title: 'Открытие. Приветствие участникам',

        href: '/papers/49/',

        startTime: '11:30',

        person: 'Софья Чебанова, Николай Пунтиков',

        flowId: [2],
        duration: 20,

        category: ''
    },

    {
        title: 'Маленькие советы дизайнерам',

        href: '/papers/46/',

        startTime: '11:50',

        person: 'Максим Ткачук',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Новое платье проектировщика: как мы создавали DaisyDisk',

        href: '/papers/40/',

        startTime: '12:00',

        person: 'Тарас Бризицкий',

        flowId: [1],
        duration: 30,

        category: 'analytics'
    },

    {
        title: 'UX исследования на всех этапах разработки продукта',

        href: '/papers/35/',

        startTime: '12:10',

        person: 'Елена Махно',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Сможет ли проектировщик взаимодействия в вебе стать проек...',

        href: '/papers/38/',

        startTime: '12:30',

        person: 'Алексей Копылов, Илья Александров',

        flowId: [2],
        duration: 30,

        category: 'ui'
    },

    {
        title: 'Быстрое прототипирование для веб и мобильных устройств',

        href: '/papers/24/',

        startTime: '13:00',

        person: 'Marcio Leibovitch',

        flowId: [2],
        duration: 40,

        category: 'ui'
    },

    {
        title: 'Обед',

        startTime: '13:40',

        flowId: [1,2,3,4],
        duration: 60,

        category: ''
    },

    {
        title: 'Сеем ветер, жнем бурю',

        href: '/papers/48/',

        startTime: '14:30',

        person: 'Иван Михайлов',

        flowId: [3],
        duration: 120,

        category: 'testing'
    },

    {
        title: 'Мастер-класс по быстрому прототипированию',

        href: '/papers/25/',

        startTime: '14:30',

        person: 'Marcio Leibovitch',

        flowId: [4],
        duration: 120,

        category: 'implementation'
    },

    {
        title: 'Секонд-хэнд проектирование',

        href: '/papers/36/',

        startTime: '14:40',

        person: 'Сергей Протопопов',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Где кончается проектирование и начинается дизайн?',

        href: '/papers/32/',

        startTime: '15:00',

        person: 'Заур Гиясов',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'NUI или почему не устанет рука',

        href: '/papers/26/',

        startTime: '15:20',

        person: 'Дмитрий Михеев',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Экранные приложения с большим количеством информации',

        href: '/papers/31/',

        startTime: '15:40',

        person: 'Николай  Слёзкинский',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Исследования интерфейсов в Яндексе',

        href: '/papers/41/',

        startTime: '16:00',

        person: 'Александр Кондратьев',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Кофе-брейк',

        startTime: '16:20',

        flowId: [1],
        duration: 30,

        category: ''
    },

    {
        title: 'Интерактив: Исследование аудитории',

        href: '/papers/47/',

        startTime: '16:40',

        person: 'Кристина Стоянова, Софья Чебанова',

        flowId: [3],
        duration: 120,

        category: 'testing'
    },

    {
        title: 'Проектирование адаптивного интерфейса',

        href: '/papers/34/',

        startTime: '16:50',

        person: 'Андрей Туркин',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Секретная техника самураев Toyota',

        href: '/papers/30/',

        startTime: '17:10',

        person: 'Рамиль Шайхутдинов',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Адаптивный дизайн? Адаптивное мышление!',

        href: '/papers/33/',

        startTime: '17:10',

        person: 'Евгений Гуринович',

        flowId: [1],
        duration: 20,

        category: 'analytics'
    },

    {
        title: 'Рука об руку с эффективностью — сплит-тесты',

        href: '/papers/42/',

        startTime: '17:30',

        person: 'Ирина Кукушкина',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Статистика без банальщины',

        href: '/papers/27/',

        startTime: '17:30',

        person: 'Иван Серебренников',

        flowId: [1],
        duration: 20,

        category: 'analytics'
    },

    {
        title: 'Взаимодействие пользователя и системы. Методики описания ...',

        href: '/papers/29/',

        startTime: '17:50',

        person: 'Маргарита Титова',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Gamification in Action',

        href: '/papers/28/',

        startTime: '18:10',

        person: 'Иво Димитров',

        flowId: [2],
        duration: 20,

        category: 'ui'
    },

    {
        title: 'Закрытие. Призы и итоги',

        startTime: '18:30',

        flowId: [2],
        duration: 30,

        category: ''
    },

    {
        title: 'Afterparty',

        startTime: '19:00',

        flowId: [1,2,3,4],
        duration: 120,

        category: ''
    }

]