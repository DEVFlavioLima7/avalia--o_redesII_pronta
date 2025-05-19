Write-Host "Qual tipo de container deseja acessar? (host/router)"
$tipo = Read-Host

Write-Host "Digite o número do container (ex: 1, 2, 3...)"
$numero = Read-Host

if ($tipo -eq "host") {
    $nome_container = "avaliao_redesii-host$numero-1"
} elseif ($tipo -eq "router") {
    $nome_container = "router_$numero"
} else {
    Write-Host "Tipo inválido. Use 'host' ou 'router'."
    exit
}

Write-Host "Acessando $nome_container..."
docker exec -it $nome_container bash
