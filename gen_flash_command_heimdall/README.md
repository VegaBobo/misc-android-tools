Ferramenta simples para gerar um comando do Heimdall que permite fazer a instalação da ROM Stock em aparelhos da Samsung.

Atualmente, você pode instalar a ROM Stock em aparelhos da Samsung usando o Heimdall no Linux, extraindo o firmware inteiro, depois conseguindo as partições do seu aparelho usando o "heimdall print-pit", por fim, é só comprar as partições do firmware extraído com as do PIT e flashar elas pelo heimdall, tipo: "heimdall flash --BOOT boot.img --SUPER super.img...", porem, fazer essa comparação é chato.

Essa ferramenta compara as partições do firmware baixado, com as do PIT, assim, gerando um comando do heimdall prontinho para você fazer a instalação da ROM Stock!

Flashando a ROM Stock:

1. Baixe a Stock da Samsung
2. Baixe e instale o Heimdall
3. Extraia todos os arquivos da ROM Stock da Samsung (extraia todos os arquivos MD5, coloque todos os arquivos LZ4 em uma unica pasta, depois execute o comando: `unlz4 -m * && rm *.lz4`)
4. Coloque seu celular em modo download, e execute: `heimdall print-pit > pit.txt`
5. Execute: `python3 gen_flash_command_heimdall.py pit.txt <Caminho do firmware extraido>`
6. Depois disso, você deve receber um retorno com o comando que devera ser executado para flashar aquele firmware, algo como:

*heimdall flash --BOOTLOADER sboot.bin --UP_PARAM up_param.bin --KEYSTORAGE keystorage.bin --UH uh.bin --DTBO dtbo.img --BOOT boot.img --RECOVERY recovery.img .....*

Execute o comando retornado e pronto, você vai conseguir flashar a Stock ROM do seu aparelho Samsung usando o Heimdall.


- Ferramenta não foi testada em vários aparelhos
- Script provavelmente falho (eu não manjo de Python ok)
'
