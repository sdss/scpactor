#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: Mingyeong YANG (mingyeong@khu.ac.kr)
# @Date: 2021-03-22
# @Filename: actor.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import asyncio
import click

@command_parser.command()
@click.argument("EXPTIME", type=float)
async def expose(command, exptime):
    """Exposes the camera."""

    command.info(text="Starting the exposure.")

    # Here we talk to the camera to initiate the exposure.
    command.info(text="power checking...")
    command.info(text="power OK")
    """
    power_cmd = await command.actor.send_command("npc_actor", "onall")
    await power_cmd  # Block until the command is done (finished or failed)
    if power_cmd.status.did_fail:
        # Do cleanup
        return command.fail(text="failed to turn on all of the NPC")
    """

    # Use command to access the actor and command the shutter
    shutter_cmd = await command.actor.send_command("shutter_actor", "open")

    await shutter_cmd  # Block until the command is done (finished or failed)
    if shutter_cmd.status.did_fail:
        # Do cleanup
        return command.fail(text="Shutter failed to open")

    # Report status of the shutter
    replies = shutter_cmd.replies
    shutter_status = replies[-1].body["shutter"]
    if shutter_status not in ["open", "closed"]:
        return command.fail(text=f"Unknown shutter status {shutter_status!r}.")

    command.info(f"Shutter is now {shutter_status!r}.")

    # Sleep until the exposure is complete.
    command.info(text="exposing by archon...")
    await asyncio.sleep(exptime)

    # Close the shutter. Note the double await.
    await (await command.actor.send_command("shutter_actor", "close"))

    # Finish exposure, read buffer, etc.

    return command.finish(text="Exposure done!")

