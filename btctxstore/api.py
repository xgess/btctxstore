#!/usr/bin/env python
# coding: utf-8
# Copyright (c) 2015 Fabian Barkhau <fabian.barkhau@gmail.com>
# License: MIT (see LICENSE file)


import sanitize
import apigen
import control
from pycoin.tx.Tx import Tx
from pycoin.serialize import b2h, h2b, b2h_rev, h2b_rev
from insight import InsightService # XXX rm when added to next pycoin version


class BtcTxStore(apigen.Definition):
    """Bitcoin nulldata output io library."""

    def __init__(self, testnet="False"):
        self.testnet = sanitize.flag(testnet)
        if self.testnet:
            self.service = InsightService("https://test-insight.bitpay.com/")
        else:
            self.service = InsightService("https://insight.bitpay.com/")

    @apigen.command()
    def writebin(self, rawtx, hexdata):
        """Writes <hexdata> as new nulldata output in <rawtx>."""
        tx = sanitize.tx(rawtx)
        nulldatatxout = sanitize.nulldatatxout(hexdata)
        tx = control.write(tx, nulldatatxout)
        return tx.as_hex()

    @apigen.command()
    def readbin(self, rawtx):
        """Returns binary nulldata from <rawtx> as hexdata."""
        tx = sanitize.tx(rawtx)
        data = control.read(tx)
        return b2h(data)

    @apigen.command()
    def createtx(self, txins, txouts, locktime="0"):
        """Create unsigned raw tx with given txins/txouts as json data.
        <txins>: '[{"txid" : hexdata, "index" : number}, ...]'
        <txouts>: '[{"address" : hexdata, "value" : satoshis}, ...]'
        """
        locktime = sanitize.positiveinteger(locktime)
        txins = sanitize.txins(txins)
        txouts = sanitize.txouts(self.testnet, txouts)
        tx = Tx(1, txins, txouts, locktime)
        return tx.as_hex()

    @apigen.command()
    def gettx(self, txid):
        txid = sanitize.txid(txid)
        tx = self.service.get_tx(txid)
        return tx.as_hex()

    @apigen.command()
    def signrawtx(self, rawtx, privatekeys): # TODO test it
        """Sign <rawtx> with  given <privatekeys> as json data.
        <privatekeys>: '[privatekeyhex, ...]'
        """
        tx = sanitize.tx(rawtx)
        secretexponents = sanitize.secretexponents(privatekeys)
        return control.signtx(self.service, tx, secretexponents).as_hex()

    @apigen.command()
    def getutxos(self, address):
        """Get current utxos for address."""
        address = sanitize.address(address)
        spendables = self.service.spendables_for_address(address)
        def reformat(spendable):
            return { 
                "txid" : b2h_rev(spendable.tx_hash), # correct?
                "index" : spendable.tx_out_index
            }
        return map(reformat, spendables)

    @apigen.command()
    def publish(self, rawtx):
        """Publish signed raw transaction to bitcoin network."""
        return "Sorry this feature is not implemented yet."

