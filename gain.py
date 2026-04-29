import frida
import psutil
import time
import sys
import os

PROCESS_NAME = "DiscordPTB.exe"
MODULE_NAME = "discord_voice.node"
OFFSET = 0x8AFCC0
gain_value = 1.0

def get_discord_pids():
    return [p.info['pid'] for p in psutil.process_iter(['pid', 'name'])
            if p.info['name'] and PROCESS_NAME.lower() in p.info['name'].lower()]


def attach_and_hook(pid):
    try:
        session = frida.attach(pid)
    except Exception:
        return None

    script = session.create_script(f"""
        var offset = {OFFSET};
        var moduleName = "{MODULE_NAME}";
        var gain = {gain_value};

        rpc.exports = {{
            setgain: function(newGain) {{
                gain = newGain;
            }}
        }};

        var interval = setInterval(function() {{
            var mod = Process.findModuleByName(moduleName);
            if (mod) {{
                var hookAddr = mod.base.add(offset);
                
                Interceptor.attach(hookAddr, {{
                    onEnter: function(args) {{
                        var samples = args[1];
                        var size = parseInt(args[2]);
                        for (var i = 0; i < size * 2; i++) {{
                            var s = samples.add(i * 2).readS16();
                            var amplified = Math.max(-32768, Math.min(32767, s * gain));
                            samples.add(i * 2).writeS16(amplified);
                        }}
                    }}
                }});

                clearInterval(interval);
            }}
        }}, 500);
    """)


    script.on("message", lambda msg, data: print("[>]", msg["payload"]))
    script.load()
    return session, script


def main():
    attached_sessions = []

    print("[*] ryze has started slapping discord...")

    try:
        while True:
            pids = get_discord_pids()
            for pid in pids:
                if pid not in [s['pid'] for s in attached_sessions]:
                    result = attach_and_hook(pid)
                    if result:
                        session, script = result
                        attached_sessions.append({'pid': pid, 'session': session, 'script': script})

            os.system("cls")
            print("[ryze gain control]")
            time.sleep(2)
            try:
                gain_input = input("enter new gain: ")
                new_gain = float(gain_input)
                for s in attached_sessions:
                    s['script'].exports_sync.setgain(new_gain)
                print("[+] gain upd")
    
            except ValueError:
                print("[-] inv input")
            except EOFError:
                break

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] exiting...")
        for s in attached_sessions:
            s['session'].detach()
        sys.exit(0)


if __name__ == "__main__":
    main()
