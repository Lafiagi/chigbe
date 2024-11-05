from algopy import Asset, Global, Txn, UInt64, arc4, gtxn, itxn, String, Account


class Chigbe(arc4.ARC4Contract):
    name: String
    manufacture_date: UInt64
    expiry_date: UInt64
    unique_code: String
    asset_id: UInt64
    batch_number: String
    manufacturer: String
    owner: String

    @arc4.abimethod(allow_actions=["NoOp"], create="require")
    def create_application(
        self,
        manufacture_date: UInt64,
        expiry_date: UInt64,
        unique_code: String,
        asset_id: UInt64,
        batch_number: String,
        manufacturer: String,
    ) -> None:
        self.asset_id = asset_id
        self.expiry_date = expiry_date
        self.unique_code = unique_code
        self.manufacture_date = manufacture_date
        self.batch_number = batch_number
        self.manufacturer = manufacturer

    @arc4.abimethod
    def authenticate_product(self, unique_code: String) -> bool:
        # check if the unique code is valid for the smart contract
        return self.unique_code == unique_code
