from pathlib import Path

from simpler.flows import ELDataFlow
from simpler.stack import DataStack


class StackBuilder(object):
    stack: DataStack

    def build(self, path: str = "./.meltano") -> None:
        """Build a Meltano project for this data stack."""
        self.compile(path=path)

    # Build to common Open Source Tools
    def compile(self, path: str = "./.meltano") -> None:
        """Build a Meltano project for this data stack."""
        self.write_manifest(path=Path("./build/stack-manifest.json"))

    # Actions

    def write_manifest(self, path: Path) -> None:
        """Write stack assets dict as json to provided file path."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            f.write(self.stack.json(indent=2))

    def run_el(self) -> None:
        """Run EL."""
        for source in self.stack.sources:
            el_flow = ELDataFlow(
                source=source,
                loader=self.stack.as_raw_loader(),
            )
            el_flow.run()

    def run_transforms(self) -> None:
        """Run transforms."""
        print("Emulating dbt transform cycle.")
        # TODO: Implement dbt transforms

    def run_elt(self) -> None:
        """Run EL."""
        self.run_el()
        self.run_transforms()

    def publish(self) -> None:
        """Publish the data stack."""
        for entity in self.stack.entities.values():
            entity.publish()

    # CLI Entrypoints

    @classmethod
    def init_and_compile(cls) -> None:
        """Compile the data stack."""
        builder = cls()
        builder.compile()
        print(builder.stack.json(indent=2))

    @classmethod
    def init_and_el(cls) -> None:
        builder = cls()
        builder.compile()
        for source in builder.stack.sources:
            el_flow = ELDataFlow(
                source=source,
                loader=builder.stack.as_raw_loader(),
            )
            el_flow.run()

    @classmethod
    def init_and_elt(cls) -> None:
        builder = cls()
        builder.compile()
        for source in builder.stack.sources:
            el_flow = ELDataFlow(
                source=source,
                loader=builder.stack.as_raw_loader(),
            )
            el_flow.run()
        builder.run_transforms()
