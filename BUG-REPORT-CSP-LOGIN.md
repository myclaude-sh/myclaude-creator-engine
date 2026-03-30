# BUG REPORT: `myclaude login` bloqueado por CSP

**Severity:** Critical — bloqueia todo o fluxo de publish
**Reportado por:** Victor (CEO) — 2026-03-28
**Ambiente:** Windows 11 Pro, Edge (browser padrão), myclaude CLI instalada via npm

---

## Resumo

O comando `myclaude login` falha porque a página de autenticação em `myclaude.sh` tem uma Content Security Policy que bloqueia o `form-action` para `localhost`. O formulário de login não consegue enviar os dados de volta para o servidor local do CLI.

## Reprodução

1. Rodar `myclaude logout` (sucesso)
2. Rodar `myclaude login`
3. Browser abre: `https://www.myclaude.sh/auth?port={PORT}&state={STATE}`
4. Usuário faz login normalmente na página
5. Ao submeter, o form tenta POST para `http://localhost:{PORT}/callback`
6. **CSP bloqueia o POST** → login nunca completa

## Erro Exato (Console do Browser)

```
Sending form data to 'http://localhost:52783/callback' violates the following
Content Security Policy directive: "form-action 'self'".
The request has been blocked.
```

Erro adicional:
```
Unchecked runtime.lastError: Could not establish connection.
Receiving end does not exist.
```

## Reproduzido 2x

| Tentativa | Porta | Estado | Resultado |
|-----------|-------|--------|-----------|
| 1 | 60721 | `78f3f4d4...` | CSP blocked |
| 2 | 52783 | `f88c74cf...` | CSP blocked |

## Causa Raiz

O header CSP de `myclaude.sh` tem:
```
Content-Security-Policy: ... form-action 'self' ...
```

Isso significa que o form só pode submeter para o próprio domínio (`myclaude.sh`). O callback para `localhost:{port}` é bloqueado porque não está na whitelist.

## Fix Necessário

Adicionar `http://localhost:*` ao `form-action` na CSP de `myclaude.sh`:

```
Content-Security-Policy: ... form-action 'self' http://localhost:* ...
```

Ou alternativamente, usar um `http://127.0.0.1:*` pattern:
```
form-action 'self' http://localhost:* http://127.0.0.1:*
```

### Alternativa (se CSP não puder ser relaxada)

Mudar o fluxo OAuth para usar **redirect** em vez de **form-action**:
- Após autenticação no server, redirecionar via `302 Location: http://localhost:{port}/callback?code=...`
- Redirects não são bloqueados por `form-action` — só forms são

Outra opção:
- Implementar `myclaude login --token` para permitir login via token copiado manualmente
- Gerar token no dashboard `myclaude.sh/settings/tokens`, usuário cola no terminal

## Impacto

- **Bloqueia 100% do fluxo de publish via CLI**
- Nenhum usuário em browser com CSP strict consegue completar `myclaude login`
- Workaround atual: nenhum (sem `--token` flag, sem alternativa)
- Produto `launch-brief` está packaged em `.publish/` esperando publish

## Contexto Adicional

- O usuário logou anteriormente como `@darwimmusic` (essa conta funcionou antes — possível que o CSP foi adicionado/modificado recentemente)
- Warnings de preload de fontes woff2 também aparecem no console (não críticos):
  - `dbe52a30e58c21fa-s.p.0j1tqrwxeg-58.woff2`
  - `797e433ab948586e-s.p.0.q-h669a_dqa.woff2`
  - `1ef31f0c5389e115-s.p.0vkirjbsp40gf.woff2`
  - `caa3a2e1cccd8315-s.p.16t1db8_9y2o~.woff2`

---

**Prioridade sugerida:** P0 — bloqueia a funcionalidade core do CLI (login → publish)
