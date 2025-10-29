# Just a script to run the examples

if __name__ == "__main__":

    from examples.create_instance import create_instance
    from examples.solve_instance import solve_instance
    from examples.experiments import exemplary_experiments

    # Run examples
    create_instance()
    solve_instance()
    exemplary_experiments()

    