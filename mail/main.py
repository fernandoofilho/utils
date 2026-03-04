import argparse
import os
import smtplib
from email.message import EmailMessage
from typing import Iterable

def enviar_email(
    assunto: str,
    corpo: str,
    destinatarios: Iterable[str],
    remetente: str,
    smtp_host: str,
    smtp_port: int = 587,
    usuario: str | None = None,
    senha: str | None = None,
    usar_tls: bool = True,
) -> None:
    """
    Função padrão para enviar e‑mail via SMTP.
    """

    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = remetente
    msg["To"] = ", ".join(destinatarios)
    msg.set_content(corpo)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        if usar_tls:
            server.starttls()

        if usuario and senha:
            server.login(usuario, senha)

        server.send_message(msg)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Envia um e‑mail simples (útil para avisar fim de scripts / status da VPS)."
    )

    parser.add_argument(
        "-s",
        "--subject",
        required=True,
        help="Assunto do e‑mail.",
    )
    parser.add_argument(
        "-b",
        "--body",
        required=True,
        help="Corpo do e‑mail (texto simples).",
    )
    parser.add_argument(
        "-t",
        "--to",
        required=True,
        nargs="+",
        help="Destinatários (um ou mais e‑mails).",
    )
    parser.add_argument(
        "-f",
        "--from-address",
        required=True,
        help="Endereço de e‑mail do remetente.",
    )

    parser.add_argument(
        "--host",
        default=os.getenv("MAIL_SMTP_HOST"),
        help="Host do servidor SMTP (ou variável MAIL_SMTP_HOST).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MAIL_SMTP_PORT", "587")),
        help="Porta do servidor SMTP (ou variável MAIL_SMTP_PORT).",
    )
    parser.add_argument(
        "--user",
        default=os.getenv("MAIL_SMTP_USER"),
        help="Usuário de autenticação SMTP (ou variável MAIL_SMTP_USER).",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("MAIL_SMTP_PASSWORD"),
        help="Senha de autenticação SMTP (ou variável MAIL_SMTP_PASSWORD).",
    )
    parser.add_argument(
        "--no-tls",
        action="store_true",
        help="Desabilita TLS (por padrão TLS é habilitado).",
    )

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if not args.host:
        parser.error("Informe o host SMTP via --host ou variável MAIL_SMTP_HOST.")

    enviar_email(
        assunto=args.subject,
        corpo=args.body,
        destinatarios=args.to,
        remetente=args.from_address,
        smtp_host=args.host,
        smtp_port=args.port,
        usuario=args.user,
        senha=args.password,
        usar_tls=not args.no_tls,
    )


if __name__ == "__main__":
    main()