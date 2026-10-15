// Endereço do webhook de vendas da Hest: https://<domínio>/api/hest/venda
// A lógica e os comentários estão em api/_lib/hest.mjs.
import { tratarVenda } from "../_lib/hest.mjs"

export function POST(request) {
  return tratarVenda(request)
}
