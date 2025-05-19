#!/bin/sh

echo "Esperando 5 segundos antes de iniciar o ping para $DESTINATION..."
sleep 5
echo "Iniciando ping para $DESTINATION"
ping -c 4 "$DESTINATION"

