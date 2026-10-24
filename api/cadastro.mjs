// Endereço do cadastro de e-mail do rodapé: https://<domínio>/api/cadastro
// A lógica e os comentários estão em api/_lib/cadastro.mjs.
import { tratarCadastro } from "./_lib/cadastro.mjs"

export function POST(request) {
  return tratarCadastro(request)
}
