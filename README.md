# ryze gain control

join: [discord](https://discord.gg/unimaginable)

people said audio hooks in python/js weren’t possible
said it had to be native, called me a clown just for even trying

so yeah, here’s the result

## what this is

real-time discord audio hook built using:

* python (process handling + control)
* javascript (injected with frida for the actual hook)

no native dlls
no magic
just understanding what you’re doing

## what it does

* finds running discord processes
* attaches using frida
* hooks the voice module
* intercepts raw audio samples
* applies live gain changes in real time

## how it works

python attaches and manages everything
js runs inside the process and hooks the function
audio buffer gets modified before output

simple

## why this exists

this was just a project i made for myself in 15 minutes.

it’s not meant to be perfect, it’s not meant to peak limits or smth

but people still started talking like it couldn’t be done at all
coping hard instead of actually trying

so now it’s public

## usage

run it
enter gain
done

## requirements

* python 3
* frida
* psutil

## note

don’t be a skid

if you’re here, learn from it
don’t just copy paste and pretend you built something

the code’s right there, what you take from it is on you

---
