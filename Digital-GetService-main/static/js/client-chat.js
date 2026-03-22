(() => {
    const layout = document.querySelector('.chat-layout');
    if (!layout) {
        return;
    }

    const currentUserId = Number(layout.dataset.currentUserId || 0);
    const csrfToken = layout.dataset.csrfToken || '';
    const apiBase = layout.dataset.apiBase || '/site/api';
    const wsUrl = layout.dataset.wsUrl || '';
    const wsToken = layout.dataset.wsToken || '';

    const messagesContainer = document.getElementById('chatMessages');
    const chatHeader = document.getElementById('chatHeader');
    const form = document.getElementById('chatForm');
    const input = document.getElementById('chatMessageInput');
    const sendButton = document.getElementById('chatSendButton');

    let adminUser = null;
    let socket = null;
    let reconnectTimer = null;
    let conversationId = null;

    const withApi = (path) => `${apiBase.replace(/\/+$/, '')}/${path.replace(/^\/+/, '')}`;

    const escapeHtml = (value) => {
        const div = document.createElement('div');
        div.textContent = value;
        return div.innerHTML;
    };

    const renderMessages = (messages) => {
        if (!messages || messages.length === 0) {
            messagesContainer.innerHTML = '<p class="text-muted small mb-0 text-center">Aucun message pour le moment. Commencez la conversation!</p>';
            return;
        }

        messagesContainer.innerHTML = messages.map((message) => {
            const bubbleType = Number(message.sender_id) === currentUserId ? 'self' : 'other';
            return `
                <div class="chat-bubble ${bubbleType}">
                    <div>${escapeHtml(message.content)}</div>
                    <span class="chat-meta">${escapeHtml(message.sender_name)} | ${escapeHtml(message.created_at)}</span>
                </div>
            `;
        }).join('');

        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };

    const findAdminUser = async () => {
        try {
            const response = await fetch(withApi('chat_admin'), { credentials: 'same-origin' });
            if (!response.ok) {
                return null;
            }
            const data = await response.json();
            return data.admin_user || null;
        } catch (error) {
            console.error('Erreur lors de la récupération de l\'admin:', error);
            return null;
        }
    };

    const loadMessages = async () => {
        if (!adminUser || !adminUser.id) {
            messagesContainer.innerHTML = '<p class="text-muted small mb-0 text-center">Aucun administrateur disponible pour le support.</p>';
            return;
        }

        try {
            const response = await fetch(withApi(`chat_fetch?target_id=${adminUser.id}`), { credentials: 'same-origin' });
            if (!response.ok) {
                return;
            }
            const data = await response.json();
            conversationId = data.conversation_id || null;
            chatHeader.textContent = `Conversation avec ${escapeHtml(data.target_user.full_name)}`;
            renderMessages(data.messages || []);
            input.disabled = false;
            sendButton.disabled = false;
        } catch (error) {
            console.error('Erreur lors du chargement des messages:', error);
        }
    };

    const notifyWsNewMessage = (targetId, conversationId, messageId) => {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            return;
        }

        socket.send(JSON.stringify({
            type: 'chat:new_message',
            target_user_id: targetId,
            sender_user_id: currentUserId,
            conversation_id: conversationId,
            message_id: messageId,
        }));
    };

    const sendMessage = async (message) => {
        if (!adminUser || !adminUser.id || !message.trim()) {
            return;
        }

        try {
            const response = await fetch(withApi('chat_send'), {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-Token': csrfToken,
                },
                body: JSON.stringify({
                    target_id: adminUser.id,
                    message: message.trim(),
                }),
            });

            if (!response.ok) {
                console.error('Erreur lors de l\'envoi du message');
                return;
            }

            const data = await response.json();
            await loadMessages();
            notifyWsNewMessage(Number(data.target_id), Number(data.conversation_id), Number(data.message_id));
        } catch (error) {
            console.error('Erreur lors de l\'envoi:', error);
        }
    };

    const handleSocketMessage = async (event) => {
        try {
            const payload = JSON.parse(event.data);
            if (!payload || payload.type !== 'chat:new_message') {
                return;
            }

            const senderId = Number(payload.sender_user_id || 0);
            const targetId = Number(payload.target_user_id || 0);
            const concernsCurrentUser = senderId === currentUserId || targetId === currentUserId;
            if (!concernsCurrentUser) {
                return;
            }

            await loadMessages();
        } catch (error) {
            // ignore malformed payload
        }
    };

    const connectWebSocket = () => {
        if (!wsUrl || !wsToken) {
            return;
        }

        try {
            const connector = wsUrl.includes('?') ? '&' : '?';
            socket = new WebSocket(`${wsUrl}${connector}token=${encodeURIComponent(wsToken)}`);
        } catch (error) {
            console.error('Erreur WebSocket:', error);
            return;
        }

        socket.addEventListener('open', () => {
            console.log('WebSocket connecté');
        });

        socket.addEventListener('message', handleSocketMessage);

        socket.addEventListener('close', () => {
            if (reconnectTimer) {
                clearTimeout(reconnectTimer);
            }
            reconnectTimer = setTimeout(connectWebSocket, 2000);
        });

        socket.addEventListener('error', () => {
            console.error('Erreur WebSocket');
        });
    };

    const initialize = async () => {
        adminUser = await findAdminUser();
        if (!adminUser) {
            messagesContainer.innerHTML = '<p class="text-muted small mb-0 text-center">Aucun administrateur disponible pour le support.</p>';
            input.disabled = true;
            sendButton.disabled = true;
            return;
        }

        await loadMessages();
        connectWebSocket();
    };

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = input.value;
        input.value = '';
        await sendMessage(message);
        input.focus();
    });

    initialize();
})();
